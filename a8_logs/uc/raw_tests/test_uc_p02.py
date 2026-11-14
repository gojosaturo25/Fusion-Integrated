"""Test cases for UC-PMS-005, UC-PMS-006, UC-PMS-007, UC-PMS-008 from UC_DESIGN.json."""
import pytest
from datetime import date, timedelta

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.response import Response

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument,
    ApplicationHistory, OfficeAction
)
from modules.patent.services.applications import (
    resubmit_application, withdraw_application, assign_director, review_application
)
from modules.patent.domain.policy import can_transition, is_conflicted, can_withdraw


# -----------------------------------------------------------------------------
# TEST-PMS-UC005-MAX: Resubmission within feedback period
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_005_max_resubmission_within_deadline():
    """TEST-PMS-UC005-MAX: Verify that Applicants can revise applications within the feedback period."""
    
    # Arrange: Create application in Needs Revision state with valid resubmission deadline
    applicant_id = 1001
    director_id = 2001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-001",
        defaults={
            'applicant_id': applicant_id,
            'status': 'needs_revision',
            'assigned_director_id': director_id,
            'review_due_date': None,
            'resubmission_deadline': date.today() + timedelta(days=30),  # Valid deadline
            'version_number': 1,
        }
    )
    
    # Create inventor for conflict testing
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Create document
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Applicant resubmits with changes addressing feedback
    changes = {
        'title': 'Revised Title',
        'description': 'Updated description addressing all concerns'
    }
    response_to_feedback = "All feedback points have been addressed in this revision."
    
    result_app = resubmit_application(
        applicant_id=applicant_id,
        application_id=app.id,
        changes=changes,
        response_to_feedback=response_to_feedback,
        actor_id=applicant_id
    )
    
    # Assert: Application status updated to Resubmitted, version bumped, history recorded
    assert result_app.status == 'resubmitted'
    assert result_app.version_number == 2
    assert result_app.resubmission_deadline is not None
    
    # Verify history entry created
    history_entries = ApplicationHistory.objects.filter(application=app)
    assert len(history_entries) > 0
    recent_history = list(history_entries).reverse()[0]
    assert recent_history.action == 'resubmit'
    assert recent_history.to_status == 'resubmitted'


# -----------------------------------------------------------------------------
# TEST-PMS-UC005-MIN: Resubmission outside deadline blocked
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_005_min_resubmission_late_deadline():
    """TEST-PMS-UC005-MIN: Verify that resubmissions outside the 60-day deadline are blocked."""
    
    # Arrange: Create application with expired resubmission deadline
    applicant_id = 1001
    director_id = 2001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-002",
        defaults={
            'applicant_id': applicant_id,
            'status': 'needs_revision',
            'assigned_director_id': director_id,
            'review_due_date': None,
            'resubmission_deadline': date.today() - timedelta(days=10),  # Expired deadline
            'version_number': 1,
        }
    )
    
    # Create inventor for conflict testing
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Applicant attempts to resubmit after deadline expired
    changes = {
        'title': 'Revised Title',
        'description': 'Updated description'
    }
    response_to_feedback = "Addressing all concerns."
    
    with pytest.raises(ValueError) as exc_info:
        resubmit_application(
            applicant_id=applicant_id,
            application_id=app.id,
            changes=changes,
            response_to_feedback=response_to_feedback,
            actor_id=applicant_id
        )
    
    # Assert: Error raised due to expired deadline
    assert "Resubmission deadline" in str(exc_info.value)
    assert "passed" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# TEST-PMS-UC005-MIN2: Resubmission ignoring feedback rejected
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_005_min2_resubmission_ignoring_feedback():
    """TEST-PMS-UC005-MIN2: Verify that resubmissions not addressing Director feedback are rejected."""
    
    # Arrange: Create application in Needs Revision state
    applicant_id = 1001
    director_id = 2001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-003",
        defaults={
            'applicant_id': applicant_id,
            'status': 'needs_revision',
            'assigned_director_id': director_id,
            'review_due_date': None,
            'resubmission_deadline': date.today() + timedelta(days=30),  # Valid deadline
            'version_number': 1,
        }
    )
    
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Applicant attempts to resubmit without addressing feedback
    changes = {
        'title': 'Same Title',  # No meaningful change
        'description': 'No changes made'
    }
    response_to_feedback = "I disagree with the feedback."  # Not addressing concerns
    
    with pytest.raises(ValueError) as exc_info:
        resubmit_application(
            applicant_id=applicant_id,
            application_id=app.id,
            changes=changes,
            response_to_feedback=response_to_feedback,
            actor_id=applicant_id
        )
    
    # Assert: Error raised due to feedback not addressed
    assert "feedback" in str(exc_info.value).lower() or "addressed" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# TEST-PMS-UC006-MAX: Withdrawal of eligible pre-filing application
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_006_max_withdraw_eligible_application():
    """TEST-PMS-UC006-MAX: Verify that Applicants can withdraw eligible pre-filing applications."""
    
    # Arrange: Create application in withdrawal-eligible state (pre-filing)
    applicant_id = 1001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-004",
        defaults={
            'applicant_id': applicant_id,
            'status': 'submitted',  # Withdrawal-eligible per BR-PMS-068
            'assigned_director_id': None,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    # Create inventor for co-inventor consent check
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Co-Inventor",
        email="coinventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Applicant withdraws application with reason
    reason = "I no longer wish to pursue this patent application."
    
    result_app = withdraw_application(
        applicant_id=applicant_id,
        application_id=app.id,
        reason=reason
    )
    
    # Assert: Application status set to Withdrawn, history recorded
    assert result_app.status == 'withdrawn'
    assert result_app.version_number == 1
    
    # Verify history entry created
    history_entries = ApplicationHistory.objects.filter(application=app)
    assert len(history_entries) > 0
    recent_history = list(history_entries).reverse()[0]
    assert recent_history.action == 'withdraw'
    assert recent_history.to_status == 'withdrawn'


# -----------------------------------------------------------------------------
# TEST-PMS-UC006-MIN: Withdrawal blocked for non-withdrawal-eligible state
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_006_min_withdraw_non_eligible_state():
    """TEST-PMS-UC006-MIN: Verify that withdrawal is blocked when application status is not withdrawal-eligible."""
    
    # Arrange: Create application in non-withdrawal-eligible state (Filed)
    applicant_id = 1001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-005",
        defaults={
            'applicant_id': applicant_id,
            'status': 'filed',  # Not withdrawal-eligible per BR-PMS-067/068
            'assigned_director_id': None,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Applicant attempts to withdraw application in Filed state
    reason = "I want to withdraw this application."
    
    with pytest.raises(ValueError) as exc_info:
        withdraw_application(
            applicant_id=applicant_id,
            application_id=app.id,
            reason=reason
        )
    
    # Assert: Error raised due to withdrawal not allowed from current status
    assert "withdrawal" in str(exc_info.value).lower()
    assert "not allowed" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# TEST-PMS-UC007-MAX: Assignment to eligible non-conflicted Director
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_007_max_assignment_to_eligible_director():
    """TEST-PMS-UC007-MAX: Verify that Submitted applications are assigned to an eligible, non-conflicted Director."""
    
    # Arrange: Create application in Submitted state
    applicant_id = 1001
    director_id = 2001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-006",
        defaults={
            'applicant_id': applicant_id,
            'status': 'submitted',
            'assigned_director_id': None,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    # Create inventor for conflict testing
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: PCC_ADMIN assigns Director (not inventor) to application
    admin_id = 3001
    
    result_app = assign_director(
        admin_id=admin_id,
        application_id=app.id,
        director_id=director_id
    )
    
    # Assert: Application status updated to Under Review, assignment recorded
    assert result_app.status == 'under_review'
    assert result_app.assigned_director_id == director_id
    
    # Verify history entry created
    history_entries = ApplicationHistory.objects.filter(application=app)
    assert len(history_entries) > 0
    recent_history = list(history_entries).reverse()[0]
    assert recent_history.action == 'assign_director'
    assert recent_history.to_status == 'under_review'


# -----------------------------------------------------------------------------
# TEST-PMS-UC007-MIN: Assignment to conflicted Director prevented
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_007_min_assignment_to_conflicted_director():
    """TEST-PMS-UC007-MIN: Verify that assignment to a conflicted Director (inventor) is prevented."""
    
    # Arrange: Create application in Submitted state with inventor as potential director
    applicant_id = 1001
    inventor_id = 2001  # This person is both inventor and would be assigned director
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-007",
        defaults={
            'applicant_id': applicant_id,
            'status': 'submitted',
            'assigned_director_id': None,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    # Create inventor record
    Inventor.objects.create(
        application=app,
        user_id=invantor_id,
        name="Conflicted Inventor",
        email="conflicted@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: PCC_ADMIN attempts to assign inventor as director
    admin_id = 3001
    
    with pytest.raises(ValueError) as exc_info:
        assign_director(
            admin_id=admin_id,
            application_id=app.id,
            director_id=invantor_id
        )
    
    # Assert: Error raised due to conflict of interest
    assert "conflict" in str(exc_info.value).lower() or "inventor" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# TEST-PMS-UC008-MAX: Director records valid technical merit decision
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_008_max_director_valid_decision():
    """TEST-PMS-UC008-MAX: Verify that Directors record valid technical merit decisions (Approve, Reject, Needs Revision)."""
    
    # Arrange: Create application in Under Review state with assigned Director
    applicant_id = 1001
    director_id = 2001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-008",
        defaults={
            'applicant_id': applicant_id,
            'status': 'under_review',
            'assigned_director_id': director_id,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Director records decision with valid justification (>= 50 characters)
    decision = 'approve'
    justification = "This application demonstrates clear novelty and non-obviousness. The technical domain is well-defined and the claims are properly drafted."
    
    result_app = review_application(
        director_id=director_id,
        application_id=app.id,
        decision=decision,
        justification=justification
    )
    
    # Assert: Decision recorded, status updated appropriately
    assert result_app.latest_decision == decision
    assert result_app.latest_justification == justification
    
    if decision == 'approve':
        assert result_app.status == 'approved'
    else:
        assert result_app.status in ['rejected', 'needs_revision']
    
    # Verify history entry created
    history_entries = ApplicationHistory.objects.filter(application=app)
    assert len(history_entries) > 0
    recent_history = list(history_entries).reverse()[0]
    assert recent_history.action == 'review'
    assert recent_history.to_status in ['approved', 'rejected', 'needs_revision']


# -----------------------------------------------------------------------------
# Helper Functions for Test Setup
# -----------------------------------------------------------------------------

def create_test_application(app_number, applicant_id, status='submitted'):
    """Helper to create a test application with minimal required data."""
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER=app_number,
        defaults={
            'applicant_id': applicant_id,
            'status': status,
            'assigned_director_id': None,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    if created:
        app.save()
    
    return app


def create_test_inventor(app, user_id, name):
    """Helper to create a test inventor."""
    Inventor.objects.create(
        application=app,
        user_id=user_id,
        name=name,
        email=f"{name.lower()}@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )


def create_test_document(app, file_name):
    """Helper to create a test document."""
    ApplicationDocument.objects.create(
        application=app,
        file_name=file_name,
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=1001,
        archived=False
    )
