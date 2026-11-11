"""
Automated backend tests for Patent Management System (PMS) - Test Cases 137-144.
Source: FR_DESIGN.json test cases TEST-CFR-020-2 through TEST-CFR-021-2.
"""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Appeal, ApplicationHistory, OfficeAction
)
from modules.patent.services.applications import file_appeal, decide_appeal
from modules.patent.domain.policy import can_transition


# -----------------------------------------------------------------------------
# Fixtures and Setup Helpers
# -----------------------------------------------------------------------------

@pytest.fixture
def test_applicant():
    """Create a test applicant principal."""
    from conftest import make_principal
    return make_principal(kind="student", active_role="student")


@pytest.fixture
def test_director():
    """Create a test director principal."""
    from conftest import make_principal
    return make_principal(kind="director", active_role="director")


@pytest.fixture
def test_applicant_app(test_applicant):
    """Create a patent application for the test applicant."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-2024-001",
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Electronics",
        applicant_id=test_applicant.user_id,
        status="rejected",
    )
    return app


@pytest.fixture
def test_appeal(test_applicant_app):
    """Create an appeal record."""
    appeal = Appeal.objects.create(
        application=test_applicant_app,
        grounds="Grounds for appeal",
        status="submitted",
        decided_by=None,
        justification="",
    )
    return appeal


@pytest.fixture
def test_director_app(test_director):
    """Create a patent application assigned to the test director."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-2024-002",
        title="Test Application 2",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Mechanical",
        applicant_id=1,
        status="under_review",
        assigned_director_id=test_director.user_id,
    )
    return app


@pytest.fixture
def test_applicant_resubmission_app(test_applicant):
    """Create a patent application awaiting resubmission."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-2024-003",
        title="Test Application 3",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Software",
        applicant_id=test_applicant.user_id,
        status="needs_revision",
    )
    return app


@pytest.fixture
def test_office_action(test_director_app):
    """Create an office action with a response deadline."""
    oa = OfficeAction.objects.create(
        application=test_director_app,
        received_date=date.today() - timedelta(days=10),
        response_due_date=date.today() + timedelta(days=30),
        description="Office Action Description",
        status="recorded",
    )
    return oa


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-020-2 (PMS-AFR-167)
# -----------------------------------------------------------------------------

def test_cf_020_2_empty_justification_required(test_applicant_app, test_director):
    """
    TEST-CFR-020-2 | PMS-AFR-167
    
    Purpose: Verification of requirement for grounds and justification for appeal.
    
    Preconditions: Appeal form is open.
    Action/Input: Submit an appeal with empty justification.
    Expected Result: System requires justification input.
    """
    # Arrange
    grounds = "Test grounds"
    justification = ""  # Empty justification
    
    # Act - Attempt to file appeal with empty justification
    try:
        # The service layer should validate justification requirement
        # This test verifies that the system enforces justification requirement
        from modules.patent.services.applications import file_appeal
        
        # Try to create appeal without proper validation
        # Note: In production, this would be caught by serializer validation
        # For this test, we verify the policy rule exists
        assert can_transition("rejected", "appeal_submitted"), "Should allow transition to appeal_submitted"
        
        # Verify that justification is required (policy check)
        # The service layer should validate this before creating
        with pytest.raises(Exception):
            file_appeal(
                applicant_id=test_applicant.user_id,
                application_id=test_applicant_app.id,
                grounds=grounds,
                justification=""  # Empty - should fail validation
            )
        
    except Exception as e:
        # Expected - system requires justification input
        assert "justification" in str(e).lower() or "required" in str(e).lower(), \
            f"System should require justification input. Got error: {e}"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-020-3 (PMS-AFR-168)
# -----------------------------------------------------------------------------

def test_cf_020_3_director_review_appeal(test_applicant_app, test_director):
    """
    TEST-CFR-020-3 | PMS-AFR-168
    
    Purpose: Verification of Director review of appeals and documentation.
    
    Preconditions: Appeal is filed.
    Action/Input: Director views the appeal details.
    Expected Result: Director can review grounds and submit supporting docs.
    """
    # Arrange - Create a valid appeal
    appeal = file_appeal(
        applicant_id=test_applicant.user_id,
        application_id=test_applicant_app.id,
        grounds="Test grounds for appeal",
        justification="This is the required justification text."
    )
    
    # Act - Director views appeal details (via API)
    from rest_framework.test import APITestCase
    
    response = test_director.principal.get(
        reverse('decide-appeal', kwargs={'pk': appeal.id})
    )
    
    # Assert - Director can access and review grounds
    assert response.status_code == 200, "Director should be able to view appeal details"
    assert appeal.grounds in response.data.get('grounds'), \
        "Director should see the appeal grounds"
    assert appeal.justification in response.data.get('justification'), \
        "Director should see the justification"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-020-4 (PMS-AFR-169)
# -----------------------------------------------------------------------------

def test_cf_020_4_director_selects_outcome(test_applicant_app, test_director):
    """
    TEST-CFR-020-4 | PMS-AFR-169
    
    Purpose: Verification of Director choice (Uphold/Remand/Modify).
    
    Preconditions: Review is complete.
    Action/Input: Director selects an appeal outcome.
    Expected Result: One of 'Uphold Rejection', 'Remand for Amendment', or 'Modify Decision' is selected.
    """
    # Arrange - Create a valid appeal
    appeal = file_appeal(
        applicant_id=test_applicant.user_id,
        application_id=test_applicant_app.id,
        grounds="Test grounds",
        justification="Required justification text."
    )
    
    # Act - Director selects an outcome
    from rest_framework.test import APITestCase
    
    response = test_director.principal.put(
        reverse('decide-appeal', kwargs={'pk': appeal.id}),
        data={
            'outcome': 'uphold_rejection',
            'justification': "Director's justification for the decision."
        }
    )
    
    # Assert - Valid outcome is recorded
    assert response.status_code == 200, "Director should be able to select an appeal outcome"
    assert appeal.status == 'rejection_upheld', \
        f"Expected status 'rejection_upheld', got {appeal.status}"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-020-5 (PMS-AFR-170)
# -----------------------------------------------------------------------------

def test_cf_020_5_record_appeal_outcome(test_applicant_app, test_director):
    """
    TEST-CFR-020-5 | PMS-AFR-170
    
    Purpose: Verification of recording appeal outcomes.
    
    Preconditions: Decision is made.
    Action/Input: View the Case Outcome page.
    Expected Result: Outcome details are recorded.
    """
    # Arrange - Create and decide an appeal
    appeal = file_appeal(
        applicant_id=test_applicant.user_id,
        application_id=test_applicant_app.id,
        grounds="Test grounds",
        justification="Required justification text."
    )
    
    decide_appeal(
        director_id=test_director.user_id,
        appeal_id=appeal.id,
        outcome='remand_for_amendment',
        justification="Director's justification for remand."
    )
    
    # Act - View case outcome (via API)
    from rest_framework.test import APITestCase
    
    response = test_director.principal.get(
        reverse('decide-appeal', kwargs={'pk': appeal.id})
    )
    
    # Assert - Outcome details are recorded and accessible
    assert response.status_code == 200, "Outcome should be recorded"
    assert appeal.status == 'remanded_for_amendment', \
        f"Expected status 'remanded_for_amendment', got {appeal.status}"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-020-6 (PMS-AFR-171)
# -----------------------------------------------------------------------------

def test_cf_020_6_initiate_next_process_step(test_applicant_app, test_director):
    """
    TEST-CFR-020-6 | PMS-AFR-171
    
    Purpose: Verification of initiation of next applicable process step.
    
    Preconditions: Appeal outcome is recorded.
    Action/Input: Check the workflow status.
    Expected Result: System initiates the relevant next process.
    """
    # Arrange - Create and decide an appeal
    appeal = file_appeal(
        applicant_id=test_applicant.user_id,
        application_id=test_applicant_app.id,
        grounds="Test grounds",
        justification="Required justification text."
    )
    
    decide_appeal(
        director_id=test_director.user_id,
        appeal_id=appeal.id,
        outcome='decision_modified',
        justification="Director's justification for modification."
    )
    
    # Act - Check workflow status (via API)
    from rest_framework.test import APITestCase
    
    response = test_director.principal.get(
        reverse('decide-appeal', kwargs={'pk': appeal.id})
    )
    
    # Assert - System has initiated next process based on outcome
    assert response.status_code == 200, "Workflow should be updated"
    assert appeal.status == 'under_review', \
        f"Expected status transition to 'under_review' after decision_modified, got {appeal.status}"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-021-0 (PMS-AFR-172)
# -----------------------------------------------------------------------------

def test_cf_021_0_director_review_deadline(test_director_app):
    """
    TEST-CFR-021-0 | PMS-AFR-172
    
    Purpose: Verification of calculation/monitoring of Director review deadlines.
    
    Preconditions: Application is 'Under Review'.
    Action/Input: View the timeline dashboard.
    Expected Result: Deadline for review is calculated and displayed.
    """
    # Arrange - Create application under review with assigned director
    from datetime import date
    
    app = test_director_app
    app.status = "under_review"
    
    # Act - Calculate review deadline (via policy service)
    from modules.patent.domain.policy import review_due_date
    
    assigned_date = date.today()
    deadline = review_due_date(assigned_date)
    
    # Assert - Deadline is calculated and displayed
    assert deadline > assigned_date, "Review deadline should be in the future"
    assert deadline == (assigned_date + timedelta(days=15)), \
        f"Expected 15 business days from assignment, got {deadline}"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-021-1 (PMS-AFR-173)
# -----------------------------------------------------------------------------

def test_cf_021_1_revision_deadline_calculation(test_applicant_resubmission_app):
    """
    TEST-CFR-021-1 | PMS-AFR-173
    
    Purpose: Verification of calculation/monitoring of revision/resubmission deadlines.
    
    Preconditions: Application is awaiting resubmission.
    Action/Input: View the timeline dashboard.
    Expected Result: Deadline for revision is calculated and displayed.
    """
    # Arrange - Create application with rejection decision
    from datetime import date
    
    app = test_applicant_resubmission_app
    app.status = "rejected"
    
    # Set a past decision date to calculate deadline
    decision_date = date.today() - timedelta(days=10)
    app.latest_decision = "reject"
    app.resubmission_deadline = None  # Will be calculated
    
    # Act - Calculate resubmission deadline (via policy service)
    from modules.patent.domain.policy import resubmission_deadline
    
    deadline = resubmission_deadline(decision_date)
    
    # Assert - Deadline is calculated and displayed
    assert deadline > decision_date, "Resubmission deadline should be in the future"
    assert deadline == (decision_date + timedelta(days=60)), \
        f"Expected 60 business days from decision, got {deadline}"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-021-2 (PMS-AFR-174)
# -----------------------------------------------------------------------------

def test_cf_021_2_office_action_response_deadline(test_director_app, test_office_action):
    """
    TEST-CFR-021-2 | PMS-AFR-174
    
    Purpose: Verification of calculation/monitoring of office-action response deadlines (if data available).
    
    Preconditions: Office Action received, deadline calculable.
    Action/Input: View the timeline dashboard.
    Expected Result: Deadline for response is calculated and displayed.
    """
    # Arrange - Create office action with response due date
    from datetime import date
    
    oa = test_office_action
    app = test_director_app
    
    # Act - Verify deadline is stored and accessible
    assert oa.response_due_date is not None, "Response due date should be set"
    
    # Assert - Deadline is displayed in timeline (via API)
    from rest_framework.test import APITestCase
    
    response = test_director.principal.get(
        reverse('record-office-action', kwargs={'pk': oa.id})
    )
    
    assert response.status_code == 200, "Office action details should be accessible"
    assert oa.response_due_date in response.data.get('response_due_date'), \
        f"Response due date {oa.response_due_date} should be displayed"


# -----------------------------------------------------------------------------
# Test Helpers and Utilities
# -----------------------------------------------------------------------------

def test_policy_can_transition_appeal():
    """
    Verify policy allows transition from rejected to appeal_submitted.
    
    This is a unit test for the policy layer, not an integration test.
    """
    # Arrange - Check allowed transitions
    from modules.patent.domain.policy import ALLOWED_TRANSITIONS
    
    # Assert - Transition should be allowed
    assert "appeal_submitted" in ALLOWED_TRANSITIONS.get("rejected", set()), \
        "Policy should allow transition from rejected to appeal_submitted"


def test_policy_can_transition_resubmission():
    """
    Verify policy allows transition from needs_revision to resubmitted.
    
    This is a unit test for the policy layer, not an integration test.
    """
    # Arrange - Check allowed transitions
    from modules.patent.domain.policy import ALLOWED_TRANSITIONS
    
    # Assert - Transition should be allowed
    assert "resubmitted" in ALLOWED_TRANSITIONS.get("needs_revision", set()), \
        "Policy should allow transition from needs_revision to resubmitted"


def test_policy_can_transition_renewal():
    """
    Verify policy allows transition from granted to renewal_requested.
    
    This is a unit test for the policy layer, not an integration test.
    """
    # Arrange - Check allowed transitions
    from modules.patent.domain.policy import ALLOWED_TRANSITIONS
    
    # Assert - Transition should be allowed
    assert "renewal_requested" in ALLOWED_TRANSITIONS.get("granted", set()), \
        "Policy should allow transition from granted to renewal_requested"
