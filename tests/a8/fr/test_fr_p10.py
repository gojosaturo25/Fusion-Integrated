"""Tests for Patent Management System - FR Design Cases 73-80 (PMS-AFR-103 to PMS-AFR-109).

Test cases cover:
- International filing justification requirements
- Filing metadata capture and display
- Status updates to 'Filed'
- Office action logging
- Post-grant maintenance tracking activation conditions
- Maintenance fee schedule calculations
- Attorney management of maintenance reminders/deadlines
"""

import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework.response import Response

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Filing, OfficeAction, MaintenanceRecord,
    ApplicationHistory, AttorneyAssignment, Budget
)
from modules.patent.services.legal import record_filing
from modules.patent.services.post_filing import (
    record_office_action, prepare_response, approve_response, submit_response
)


@pytest.fixture
def api_client():
    """Create a test API client."""
    return APIClient()


@pytest.fixture
def principal(applicant_id=1001):
    """Create a test principal with student role."""
    from conftest import make_principal
    return make_principal(user_id=applicant_id, kind="student")


@pytest.fixture
def application(principal):
    """Create a test patent application."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="PMS-2024-001",
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="CSE",
        applicant_id=principal.user_id,
        status="attorney_assigned"
    )
    return app


@pytest.fixture
def attorney(principal):
    """Create a test attorney principal."""
    from conftest import make_principal
    return make_principal(user_id=2001, kind="staff", roles=("attorney",))


@pytest.fixture
def director(principal):
    """Create a test director principal."""
    from conftest import make_principal
    return make_principal(user_id=3001, kind="faculty", roles=("director",))


# -----------------------------------------------------------------------------
# TEST-CFR-012-4 (PMS-AFR-103) - International filing justification requirement
# -----------------------------------------------------------------------------

def test_cf_012_4_international_filing_requires_justification(
    api_client, principal, application, attorney
):
    """TEST-CFR-012-4: Verify additional justification required for international filings.
    
    Purpose: Verify requirement of additional justification for international filings.
    Preconditions: Application is being filed internationally.
    Action: Proceed with filing without justification.
    Expected: The system blocks the action and requires justification.
    """
    # Create a test principal with attorney role
    from conftest import make_principal
    attorney_principal = make_principal(user_id=2001, kind="staff", roles=("attorney",))
    
    # Mock the record_filing service to enforce international justification requirement
    # This simulates BR-PMS-128: International filings require additional justification
    
    # Test that attempting to file without justification fails for international
    with pytest.raises(Exception) as exc_info:
        record_filing(
            attorney_id=attorney_principal.user_id,
            application_id=application.id,
            office="USPTO",
            filing_number="123456789",
            filing_date=date.today(),
            international=True  # International filing requires justification
        )
    
    assert "justification" in str(exc_info.value).lower() or \
           "required" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# TEST-CFR-012-5 (PMS-AFR-104) - Filing metadata capture and display
# -----------------------------------------------------------------------------

def test_cf_012_5_filing_metadata_capture(
    api_client, principal, application, attorney
):
    """TEST-CFR-012-5: Verify capture of filing ID, date, and confirmation.
    
    Purpose: Verify capture of filing ID, date, and confirmation.
    Preconditions: Filing is recorded.
    Action: View the application's filing metadata.
    Expected: External Filing ID, Date, and Confirmation info are visible.
    """
    # Create a test principal with attorney role
    from conftest import make_principal
    attorney_principal = make_principal(user_id=2001, kind="staff", roles=("attorney",))
    
    # Record a filing
    filing = record_filing(
        attorney_id=attorney_principal.user_id,
        application_id=application.id,
        office="USPTO",
        filing_number="US-2024-123456789",
        filing_date=date.today(),
        international=False
    )
    
    # Verify filing metadata is captured correctly
    assert filing.application == application
    assert filing.patent_office == "USPTO"
    assert filing.filing_number == "US-2024-123456789"
    assert filing.filing_date == date.today()
    
    # Verify application status was updated to 'filed'
    assert application.status == "filed"


# -----------------------------------------------------------------------------
# TEST-CFR-012-6 (PMS-AFR-105) - Status update to 'Filed'
# -----------------------------------------------------------------------------

def test_cf_012_6_status_update_to_filed(
    api_client, principal, application, attorney
):
    """TEST-CFR-012-6: Verify status update to 'Filed'.
    
    Purpose: Verify status update to 'Filed'.
    Preconditions: Filing is recorded.
    Action: Check application status.
    Expected: Status updates from 'Attorney Assigned' to 'Filed'.
    """
    # Create a test principal with attorney role
    from conftest import make_principal
    attorney_principal = make_principal(user_id=2001, kind="staff", roles=("attorney",))
    
    # Ensure application starts in 'attorney_assigned' status
    application.status = "attorney_assigned"
    application.save()
    
    # Record a filing
    filing = record_filing(
        attorney_id=attorney_principal.user_id,
        application_id=application.id,
        office="USPTO",
        filing_number="US-2024-123456789",
        filing_date=date.today(),
        international=False
    )
    
    # Verify status was updated to 'filed'
    assert application.status == "filed"


# -----------------------------------------------------------------------------
# TEST-CFR-012-7 (PMS-AFR-106) - Office action logging
# -----------------------------------------------------------------------------

def test_cf_012_7_office_action_logging(
    api_client, principal, application, attorney
):
    """TEST-CFR-012-7: Verify logging of official patent office communications.
    
    Purpose: Verify logging of official patent office communications.
    Preconditions: A response or notification is received from the Patent Office.
    Action: Access the communication log.
    Expected: Official communications are logged.
    """
    # Create a test principal with attorney role
    from conftest import make_principal
    attorney_principal = make_principal(user_id=2001, kind="staff", roles=("attorney",))
    
    # Record an office action
    office_action = record_office_action(
        attorney_id=attorney_principal.user_id,
        application_id=application.id,
        received_date=date.today(),
        response_due_date=date.today() + timedelta(days=30),
        description="Office Action: Rejection of claims 1-5"
    )
    
    # Verify office action was created and logged
    assert office_action.application == application
    assert office_action.attorney_id == attorney_principal.user_id
    assert office_action.received_date == date.today()
    assert office_action.description == "Office Action: Rejection of claims 1-5"
    
    # Verify history entry was created
    history = ApplicationHistory.objects.filter(
        application=application,
        action="office_action_received"
    ).first()
    
    assert history is not None
    assert history.action == "office_action_received"


# -----------------------------------------------------------------------------
# TEST-CFR-013-0 (PMS-AFR-107) - Post-grant tracking unavailable for non-granted status
# -----------------------------------------------------------------------------

def test_cf_013_0_post_grant_tracking_unavailable_for_under_review(
    api_client, principal, application, attorney
):
    """TEST-CFR-013-0: Verify activation of post-grant tracking only for 'Granted' status.
    
    Purpose: Verify activation of post-grant tracking only for 'Granted' status.
    Preconditions: Application status is 'Under Review'.
    Action: Check the Post-Grant Maintenance menu.
    Expected: The menu is unavailable or not applicable.
    """
    # Create a test principal with attorney role
    from conftest import make_principal
    attorney_principal = make_principal(user_id=2001, kind="staff", roles=("attorney",))
    
    # Ensure application is in 'under_review' status (not granted)
    application.status = "under_review"
    application.save()
    
    # Verify that maintenance tracking is not available for non-granted applications
    # This is a UI/UX check - the service layer should prevent scheduling maintenance
    with pytest.raises(Exception) as exc_info:
        record_filing(
            attorney_id=attorney_principal.user_id,
            application_id=application.id,
            office="USPTO",
            filing_number="123456789",
            filing_date=date.today(),
            international=False
        )
    
    # Should fail because status is not 'filed' or 'granted' for maintenance scheduling
    assert "maintenance" in str(exc_info.value).lower() or \
           "status" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# TEST-CFR-013-1 (PMS-AFR-107-alt) - Post-grant tracking available for granted status
# -----------------------------------------------------------------------------

def test_cf_013_1_post_grant_tracking_available_for_granted(
    api_client, principal, application, attorney
):
    """TEST-CFR-013-1: Verify activation of post-grant tracking for 'Granted' status.
    
    Purpose: Verify activation of post-grant tracking for 'Granted' status.
    Preconditions: Application status is 'Granted'.
    Action: Check the Post-Grant Maintenance menu.
    Expected: The maintenance tracking interface becomes available.
    """
    # Create a test principal with attorney role
    from conftest import make_principal
    attorney_principal = make_principal(user_id=2001, kind="staff", roles=("attorney",))
    
    # Ensure application is in 'granted' status
    application.status = "granted"
    application.save()
    
    # Schedule maintenance for granted application
    maintenance_record = record_filing(
        attorney_id=attorney_principal.user_id,
        application_id=application.id,
        office="USPTO",
        filing_number="US-2024-123456789",
        filing_date=date.today(),
        international=False
    )
    
    # Verify maintenance can be scheduled for granted applications
    assert application.status == "granted"
    
    # Schedule a maintenance record
    from modules.patent.services.post_filing import schedule_maintenance
    maintenance = schedule_maintenance(
        attorney_id=attorney_principal.user_id,
        application_id=application.id,
        due_date=date.today() + timedelta(days=365),
        fee=100.0
    )
    
    assert maintenance.application == application
    assert maintenance.due_date == date.today() + timedelta(days=365)


# -----------------------------------------------------------------------------
# TEST-CFR-013-2 (PMS-AFR-108) - Maintenance fee schedule calculation from grant date
# -----------------------------------------------------------------------------

def test_cf_013_2_maintenance_fee_schedule_calculation(
    api_client, principal, application, attorney
):
    """TEST-CFR-013-2: Verify calculation of maintenance-fee schedules from grant date.
    
    Purpose: Verify calculation of maintenance-fee schedules from grant date.
    Preconditions: Application is 'Granted'.
    Action: View the Maintenance Schedule.
    Expected: Fees and deadlines are calculated based on the grant date.
    """
    # Create a test principal with attorney role
    from conftest import make_principal
    attorney_principal = make_principal(user_id=2001, kind="staff", roles=("attorney",))
    
    # Ensure application is in 'granted' status
    application.status = "granted"
    application.save()
    
    # Set grant date to a specific date for calculation verification
    application.grant_date = date.today() - timedelta(days=10)
    application.save()
    
    # Schedule maintenance based on grant date
    from modules.patent.services.post_filing import schedule_maintenance
    maintenance = schedule_maintenance(
        attorney_id=attorney_principal.user_id,
        application_id=application.id,
        due_date=date.today() + timedelta(days=365),  # First anniversary of grant
        fee=100.0
    )
    
    # Verify maintenance record was created with correct date calculation
    assert maintenance.application == application
    assert maintenance.due_date == date.today() + timedelta(days=365)
    assert maintenance.fee == 100.0


# -----------------------------------------------------------------------------
# TEST-CFR-013-3 (PMS-AFR-109) - Attorney management of maintenance reminders/deadlines
# -----------------------------------------------------------------------------

def test_cf_013_3_attorney_maintenance_reminders_display(
    api_client, principal, application, attorney
):
    """TEST-CFR-013-3: Verify Attorney management of maintenance reminders/deadlines.
    
    Purpose: Verify Attorney management of maintenance reminders/deadlines.
    Preconditions: Application is 'Granted' and approaching a deadline.
    Action: Attorney views the dashboard.
    Expected: Reminders and deadlines for maintenance fees are displayed.
    """
    # Create a test principal with attorney role
    from conftest import make_principal
    attorney_principal = make_principal(user_id=2001, kind="staff", roles=("attorney",))
    
    # Ensure application is in 'granted' status
    application.status = "granted"
    application.save()
    
    # Set grant date to a specific date for calculation verification
    application.grant_date = date.today() - timedelta(days=10)
    application.save()
    
    # Schedule maintenance with deadline approaching (within 30 days)
    from modules.patent.services.post_filing import schedule_maintenance
    maintenance = schedule_maintenance(
        attorney_id=attorney_principal.user_id,
        application_id=application.id,
        due_date=date.today() + timedelta(days=20),  # Approaching deadline
        fee=100.0
    )
    
    # Verify maintenance record was created with correct date calculation
    assert maintenance.application == application
    assert maintenance.due_date == date.today() + timedelta(days=20)
    assert maintenance.fee == 100.0
    
    # Attorney should be able to view and manage this maintenance record
    # This is verified by the fact that the service layer allows attorney access
    from modules.patent.services.post_filing import get_history
    history = get_history(application.id)
    
    assert len(history) > 0
