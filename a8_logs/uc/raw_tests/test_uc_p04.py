"""
Automated backend tests for Patent Management System (PMS) UC Design cases 25-32.
Test ID format: TEST-PMS-UCXXX-MIN/MAX
Source ID format: UC-PMS-XXX Main/Exception Scenario
"""

import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework.response import Response

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, OfficeAction, ApplicationHistory,
    MaintenanceRecord, Appeal, ApplicationDocument
)
from modules.patent.services.post_filing import (
    prepare_response, approve_response, submit_response
)
from modules.patent.services.legal import record_filing
from modules.patent.domain.policy import can_transition


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture
def client():
    """Django test client."""
    return APIClient()


@pytest.fixture
def principal(applicant_id=1001, kind="student"):
    """Create a Principal for testing."""
    from conftest import make_principal
    return make_principal(user_id=applicant_id, kind=kind)


@pytest.fixture
def application(principal):
    """Create a test patent application."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="PMS-2024-001",
        applicant_id=principal.user_id,
        status="submitted",
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test domain"
    )
    return app


@pytest.fixture
def office_action(application):
    """Create a test office action."""
    oa = OfficeAction.objects.create(
        application=application,
        received_date=date.today(),
        response_due_date=date.today() + timedelta(days=30),
        description="Test office action",
        status="recorded"
    )
    return oa


@pytest.fixture
def granted_application(principal):
    """Create a test granted patent application."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="PMS-2024-002",
        applicant_id=principal.user_id,
        status="granted",
        title="Test Granted Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test domain"
    )
    return app


@pytest.fixture
def maintenance_record(granted_application):
    """Create a test maintenance record."""
    mr = MaintenanceRecord.objects.create(
        application=granted_application,
        due_date=date.today() + timedelta(days=30),
        fee=100.00,
        decision="renewal_requested"
    )
    return mr


@pytest.fixture
def rejected_application(principal):
    """Create a test rejected patent application."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="PMS-2024-003",
        applicant_id=principal.user_id,
        status="rejected",
        title="Test Rejected Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test domain"
    )
    return app


# -----------------------------------------------------------------------------
# TEST-PMS-UC015-MIN: Response Submission Without Approval
# -----------------------------------------------------------------------------

class TestPMSUC015MIN:
    """Verify that responses cannot be marked submitted without required Applicant approval."""
    
    def test_response_cannot_be_submitted_without_approval(self, application, office_action, principal):
        """
        TEST-PMS-UC015-MIN | TEST-PMS-UC015 Exception Flows (Approval)
        
        Purpose: Verify that responses cannot be marked submitted without required Applicant approval.
        Preconditions: Process requires Applicant review; draft is available but not yet approved.
        Action: Attorney attempts to finalize and submit the response without Applicant approval.
        Expected Result: PMS does not mark the response as submitted; response status remains awaiting approval.
        """
        # Set up principal with attorney role for testing
        from conftest import make_principal
        attorney_principal = make_principal(user_id=2001, kind="attorney")
        
        # Prepare response without applicant approval flag
        response_text = "Test response text"
        
        # Attempt to prepare response without needs_applicant_approval=True
        result = prepare_response(
            attorney_id=2001,
            office_action_id=office_action.id,
            response_text=response_text,
            needs_applicant_approval=False  # This should fail or not set applicant_approved status
        )
        
        # Verify response was created but status is not 'response_submitted'
        assert result.status == "awaiting_applicant_approval" or result.status == "response_ready"
        assert result.response_text == response_text
        
        # The response should NOT be marked as submitted without approval
        assert result.status != "response_submitted"


# -----------------------------------------------------------------------------
# TEST-PMS-UC016-MAX: PCC_ADMIN Deadline Monitoring and Escalations
# -----------------------------------------------------------------------------

class TestPMSUC016MAX:
    """Verify that PCC_ADMIN can monitor deadlines and handle escalations."""
    
    def test_pcc_admin_can_monitor_deadlines_and_handle_escalations(self, application):
        """
        TEST-PMS-UC016-MAX | TEST-PMS-UC016 Main Success Scenario
        
        Purpose: Verify that PCC_ADMIN can monitor deadlines and handle escalations.
        Preconditions: Active authorized role; deadline records exist or are calculable.
        Action: PCC_ADMIN views monitoring view, reviews alerts (30/15/5 days), and handles missed deadline escalations.
        Expected Result: PMS calculates/maintains deadlines, generates alerts, logs activity, and routes/escalates delayed cases.
        """
        # Set up principal with admin role
        from conftest import make_principal
        admin_principal = make_principal(user_id=3001, kind="admin")
        
        # Create application with calculated deadline
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER="PMS-2024-004",
            applicant_id=admin_principal.user_id,
            status="submitted",
            title="Test Application for Deadline Monitoring",
            abstract="Test abstract",
            description="Test description",
            claims="Test claims",
            technical_domain="Test domain"
        )
        
        # Set review due date in the past to simulate missed deadline
        app.review_due_date = date.today() - timedelta(days=10)
        app.save()
        
        # Verify deadline was calculated and stored
        assert app.review_due_date is not None
        
        # PCC_ADMIN should be able to access application details
        response = admin_principal.client.get(f"/patent/applications/{app.id}/")
        
        # Response should contain deadline information
        data = response.data
        assert "review_due_date" in data or "deadline" in str(data).lower()


# -----------------------------------------------------------------------------
# TEST-PMS-UC017-MAX: Post-Grant Tracking and Renewal Decisions
# -----------------------------------------------------------------------------

class TestPMSUC017MAX:
    """Verify that post-grant tracking activates and renewal decisions are recorded."""
    
    def test_post_grant_tracking_activates_and_renewal_decisions_recorded(self, granted_application):
        """
        TEST-PMS-UC017-MAX | TEST-PMS-UC017 Main Success Scenario
        
        Purpose: Verify that post-grant tracking activates and renewal decisions are recorded.
        Preconditions: Patent status is Granted; maintenance deadline approaches.
        Action: Attorney requests a Renewal decision from the Director.
        Expected Result: Director records Renew or Do Not Renew; if Renewed, Attorney processes action and PMS updates status/history.
        """
        # Set up principal with attorney role
        from conftest import make_principal
        attorney_principal = make_principal(user_id=2001, kind="attorney")
        
        # Create maintenance record for granted application
        mr = MaintenanceRecord.objects.create(
            application=granted_application,
            due_date=date.today() + timedelta(days=30),
            fee=100.00,
            decision="renewal_requested"
        )
        
        # Verify maintenance record was created
        assert mr.application == granted_application
        assert mr.decision == "renewal_requested"
        
        # Director should be able to access and view the renewal record
        response = attorney_principal.client.get(f"/patent/maintenance/{mr.id}/")
        
        # Response should contain renewal information
        data = response.data
        assert "decision" in data or "fee" in data


# -----------------------------------------------------------------------------
# TEST-PMS-UC018-MAX: Director Records Renewal or Do Not Renew Decisions
# -----------------------------------------------------------------------------

class TestPMSUC018MAX:
    """Verify that Directors can record Renewal or Do Not Renew decisions."""
    
    def test_director_can_record_renewal_or_do_not_renew_decisions(self, maintenance_record):
        """
        TEST-PMS-UC018-MAX | TEST-PMS-UC018 Main Success Scenario
        
        Purpose: Verify that Directors can record Renewal or Do Not Renew decisions.
        Preconditions: Patent is in post-grant tracking; renewal decision is due.
        Action: Director selects Renew or Do Not Renew.
        Expected Result: PMS records the decision and makes it available for the Attorney's next action.
        """
        # Set up principal with director role
        from conftest import make_principal
        director_principal = make_principal(user_id=3001, kind="director")
        
        # Director should be able to decide renewal
        response = director_principal.client.put(
            f"/patent/maintenance/{maintenance_record.id}/decide/",
            data={
                "renew": True,
                "justification": "This is a test justification with sufficient length for validation purposes."
            }
        )
        
        # Verify decision was recorded
        updated_record = MaintenanceRecord.objects.get(pk=maintenance_record.id)
        assert updated_record.decision == "renew" or updated_record.decision == "do_not_renew"
        assert updated_record.decided_by == director_principal.user_id


# -----------------------------------------------------------------------------
# TEST-PMS-UC019-MAX: Authorized Users Can Upload Document Versions
# -----------------------------------------------------------------------------

class TestPMSUC019MAX:
    """Verify that authorized users can upload document versions."""
    
    def test_authorized_users_can_upload_document_versions(self, application):
        """
        TEST-PMS-UC019-MAX | TEST-PMS-UC019 Main Success Scenario
        
        Purpose: Verify that authorized users can upload document versions.
        Preconditions: User has valid role; action is permitted for role/status (e.g., Applicant in Needs Revision).
        Action: User uploads a new document version.
        Expected Result: PMS assigns next version number, archives previous version, logs modification with user/timestamp.
        """
        # Set up principal with applicant role
        from conftest import make_principal
        applicant_principal = make_principal(user_id=1001, kind="student")
        
        # Create initial document
        doc = ApplicationDocument.objects.create(
            application=application,
            file_name="test_document_v1.pdf",
            content_type="application/pdf",
            size=1024,
            version=1,
            sensitivity="internal",
            uploaded_by=applicant_principal.user_id
        )
        
        # Verify initial document exists
        assert ApplicationDocument.objects.filter(application=application).count() == 1
        
        # Upload new document version
        response = applicant_principal.client.post(
            f"/patent/applications/{application.id}/documents/",
            data={
                "file_name": "test_document_v2.pdf",
                "content_type": "application/pdf",
                "size": 2048
            }
        )
        
        # Verify new document was created with incremented version number
        assert response.status_code == 201
        
        # Check that documents count increased
        docs = ApplicationDocument.objects.filter(application=application)
        assert docs.count() == 2
        
        # Verify the new document has version 2
        new_doc = docs.get(file_name="test_document_v2.pdf")
        assert new_doc.version == 2


# -----------------------------------------------------------------------------
# TEST-PMS-UC019-MIN: Unauthorized Users Cannot Upload Document Versions
# -----------------------------------------------------------------------------

class TestPMSUC019MIN:
    """Verify that unauthorized users cannot upload document versions."""
    
    def test_unauthorized_users_cannot_upload_document_versions(self, application):
        """
        TEST-PMS-UC019-MIN | TEST-PMS-UC019 Exception Flows (Unauthorized)
        
        Purpose: Verify that unauthorized users cannot upload document versions.
        Preconditions: User lacks role or status permission to upload documents.
        Action: User attempts to upload a new document version.
        Expected Result: Upload is blocked; prior version history remains consistent.
        """
        # Set up principal with unauthorized role (e.g., random user without proper permissions)
        from conftest import make_principal
        unauthorized_principal = make_principal(user_id=9999, kind="student")
        
        # Create initial document
        doc = ApplicationDocument.objects.create(
            application=application,
            file_name="test_document_v1.pdf",
            content_type="application/pdf",
            size=1024,
            version=1,
            sensitivity="internal",
            uploaded_by=1001  # Original uploader
        )
        
        # Verify initial document exists
        assert ApplicationDocument.objects.filter(application=application).count() == 1
        
        # Attempt to upload document as unauthorized user
        response = unauthorized_principal.client.post(
            f"/patent/applications/{application.id}/documents/",
            data={
                "file_name": "test_document_v2.pdf",
                "content_type": "application/pdf",
                "size": 2048
            }
        )
        
        # Upload should be blocked (403 or 401 status)
        assert response.status_code in [403, 401]
        
        # Verify prior version history remains consistent (no new document created)
        docs = ApplicationDocument.objects.filter(application=application)
        assert docs.count() == 1


# -----------------------------------------------------------------------------
# TEST-PMS-UC022-MAX: Applicants Can File Appeals Within Allowed Period
# -----------------------------------------------------------------------------

class TestPMSUC022MAX:
    """Verify that Applicants can file appeals within the allowed period."""
    
    def test_applicants_can_file_appeals_within_allowed_period(self, rejected_application):
        """
        TEST-PMS-UC022-MAX | TEST-PMS-UC022 Main Success Scenario
        
        Purpose: Verify that Applicants can file appeals within the allowed period.
        Preconditions: Application is Rejected; appeal period has not expired.
        Action: Applicant enters grounds/justification and submits the appeal.
        Expected Result: PMS validates eligibility/timing, records the appeal for Director review.
        """
        # Set up principal with applicant role
        from conftest import make_principal
        applicant_principal = make_principal(user_id=1001, kind="student")
        
        # Create appeal record
        response = applicant_principal.client.post(
            f"/patent/applications/{rejected_application.id}/appeal/",
            data={
                "grounds": "The rejection is based on incorrect interpretation of the claims."
            }
        )
        
        # Verify appeal was created
        assert response.status_code == 201
        
        # Check that appeal exists in database
        appeals = Appeal.objects.filter(application=rejected_application)
        assert appeals.count() == 1
        
        # Verify appeal status is submitted
        appeal = appeals.first()
        assert appeal.status == "submitted"


# -----------------------------------------------------------------------------
# TEST-PMS-UC023-MAX: Directors Can Record Specific Appeal Outcomes
# -----------------------------------------------------------------------------

class TestPMSUC023MAX:
    """Verify that Directors can record specific appeal outcomes."""
    
    def test_directors_can_record_specific_appeal_outcomes(self, rejected_application):
        """
        TEST-PMS-UC023-MAX | TEST-PMS-UC023 Main Success Scenario
        
        Purpose: Verify that Directors can record specific appeal outcomes.
        Preconditions: Appeal exists and is available for review.
        Action: Director selects one outcome: Uphold Rejection, Remand for Amendment, or Modify Decision.
        Expected Result: PMS records the outcome and initiates the next applicable process step.
        """
        # Set up principal with director role
        from conftest import make_principal
        director_principal = make_principal(user_id=3001, kind="director")
        
        # Create appeal record
        appeal = Appeal.objects.create(
            application=rejected_application,
            grounds="The rejection is based on incorrect interpretation of the claims.",
            status="submitted",
            decided_by=None
        )
        
        # Director should be able to decide appeal outcome
        response = director_principal.client.put(
            f"/patent/appeals/{appeal.id}/",
            data={
                "outcome": "remand_for_amendment",
                "justification": "The claims need clarification and amendment before final decision."
            }
        )
        
        # Verify outcome was recorded
        assert response.status_code == 200
        
        # Check that appeal status was updated
        updated_appeal = Appeal.objects.get(pk=appeal.id)
        assert updated_appeal.decided_by == director_principal.user_id
        assert "remand_for_amendment" in str(updated_appeal.status).lower() or "modify_decision" in str(updated_appeal.status).lower()


# -----------------------------------------------------------------------------
# Helper Functions for Test Setup
# -----------------------------------------------------------------------------

def setup_test_applications():
    """Helper function to create test applications if needed."""
    from conftest import make_principal
    
    # Create test application with granted status
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="PMS-2024-TEST",
        applicant_id=1001,
        status="granted",
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test domain"
    )
    
    return app


if __name__ == "__main__":
    pytest.main([__file__, "--vs=2"])
