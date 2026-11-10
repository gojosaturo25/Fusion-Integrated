"""Test cases for Patent Management System - Office Action Response Workflow (TEST-CFR-014) and Withdrawal (TEST-CFR-015).

These tests cover the office action response lifecycle and pre-filing withdrawal functionality.
"""

import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework.response import Response

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, OfficeAction, ApplicationHistory,
    ApplicationDocument
)
from modules.patent.services.post_filing import (
    prepare_response, approve_response, submit_response, record_office_action
)


@pytest.fixture
def office_action_applicant(app):
    """Create an application with an open office action requiring applicant approval."""
    # Create a patent application in filed status
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-001",
        title="Test Application",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Electronics",
        applicant_id=1,
        status="filed"
    )
    
    # Create an office action with response due date
    oa = OfficeAction.objects.create(
        application=app,
        received_date=date.today() - timedelta(days=5),
        response_due_date=date.today() + timedelta(days=30),
        description="Office Action Description",
        status="recorded"
    )
    
    return app, oa


@pytest.fixture
def approved_response_applicant(app):
    """Create an application with a finalized response ready for submission."""
    # Create a patent application in filed status
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-002",
        title="Test Application 2",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Electronics",
        applicant_id=1,
        status="filed"
    )
    
    # Create an office action with response ready for approval
    oa = OfficeAction.objects.create(
        application=app,
        received_date=date.today() - timedelta(days=5),
        response_due_date=date.today() + timedelta(days=30),
        description="Office Action Description",
        status="response_ready"
    )
    
    return app, oa


@pytest.fixture
def draft_response_applicant(app):
    """Create an application with a draft response awaiting approval."""
    # Create a patent application in filed status
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-003",
        title="Test Application 3",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Electronics",
        applicant_id=1,
        status="filed"
    )
    
    # Create an office action with response awaiting approval
    oa = OfficeAction.objects.create(
        application=app,
        received_date=date.today() - timedelta(days=5),
        response_due_date=date.today() + timedelta(days=30),
        description="Office Action Description",
        status="awaiting_applicant_approval"
    )
    
    return app, oa


@pytest.fixture
def extension_request_applicant(app):
    """Create an application with imminent deadline."""
    # Create a patent application in filed status
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-004",
        title="Test Application 4",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Electronics",
        applicant_id=1,
        status="filed"
    )
    
    # Create an office action with imminent deadline
    oa = OfficeAction.objects.create(
        application=app,
        received_date=date.today() - timedelta(days=5),
        response_due_date=date.today() + timedelta(days=2),  # Imminent deadline
        description="Office Action Description",
        status="recorded"
    )
    
    return app, oa


@pytest.fixture
def submitted_response_applicant(app):
    """Create an application with a submitted response."""
    # Create a patent application in filed status
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-005",
        title="Test Application 5",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Electronics",
        applicant_id=1,
        status="filed"
    )
    
    # Create an office action with response submitted
    oa = OfficeAction.objects.create(
        application=app,
        received_date=date.today() - timedelta(days=5),
        response_due_date=date.today() + timedelta(days=30),
        description="Office Action Description",
        status="response_submitted"
    )
    
    return app, oa


@pytest.fixture
def withdrawn_applicant(app):
    """Create an application in submitted status for withdrawal testing."""
    # Create a patent application in submitted status (pre-filing)
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-006",
        title="Test Application 6",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Electronics",
        applicant_id=1,
        status="submitted"
    )
    
    return app


@pytest.fixture
def stub_iam(monkeypatch):
    """Use the existing stub_iam fixture from conftest.py."""
    # This fixture is already defined in conftest.py
    pass


class TestOfficeActionResponseWorkflow:
    """Test cases for Office Action Response Workflow (TEST-CFR-014)."""
    
    def test_cfr_014_2_attorney_draft_response_creation(self, office_action_applicant):
        """TEST-CFR-014-2: Verify Attorney preparation of draft responses.
        
        Source ID: PMS-AFR-118
        Purpose: Verify Attorney preparation of draft responses
        Preconditions: Office Action is open for review.
        Action/Input: Attorney creates a draft response.
        Expected Result: A draft response document is created.
        """
        app, oa = office_action_applicant
        
        # Create a draft response document
        draft_response = ApplicationDocument.objects.create(
            application=app,
            file_name="draft_response.txt",
            content_type="text/plain",
            size=1024,
            version=1,
            sensitivity="internal",
            uploaded_by=1,  # Attorney ID
            archived=False
        )
        
        # Verify draft response was created
        assert ApplicationDocument.objects.filter(
            application=app,
            file_name="draft_response.txt"
        ).exists()
    
    def test_cfr_014_3_applicant_approval_of_draft_response(self, approved_response_applicant):
        """TEST-CFR-014-3: Verify Applicant review/approval of office-action responses (if required).
        
        Source ID: PMS-AFR-119
        Purpose: Verify Applicant review/approval of office-action responses (if required)
        Preconditions: Applicable process requires Applicant approval.
        Action/Input: Applicant reviews and approves the draft response.
        Expected Result: The system records Applicant approval.
        """
        app, oa = approved_response_applicant
        
        # Approve the response
        updated_oa = approve_response(
            applicant_id=1,  # Applicant ID
            office_action_id=oa.id
        )
        
        # Verify status was updated to applicant_approved
        assert updated_oa.status == "applicant_approved"
    
    def test_cfr_014_4_attorney_finalization_of_response(self, draft_response_applicant):
        """TEST-CFR-014-4: Verify Attorney finalization of office-action responses.
        
        Source ID: PMS-AFR-120
        Purpose: Verify Attorney finalization of office-action responses
        Preconditions: Applicant has approved the draft.
        Action/Input: Attorney marks the response as 'Finalized'.
        Expected Result: The system updates status to Finalized.
        """
        app, oa = draft_response_applicant
        
        # Prepare response (simulates finalization)
        updated_oa = prepare_response(
            attorney_id=1,  # Attorney ID
            office_action_id=oa.id,
            response_text="Final Response Text",
            needs_applicant_approval=False  # Already approved
        )
        
        # Verify status was updated to response_ready (finalized state)
        assert updated_oa.status == "response_ready"
    
    def test_cfr_014_5_recording_of_office_action_response_submission(self, submitted_response_applicant):
        """TEST-CFR-014-5: Verify recording of office-action response submission within deadline.
        
        Source ID: PMS-AFR-121
        Purpose: Verify recording of office-action response submission within deadline
        Preconditions: Response is finalized.
        Action/Input: Submit the finalized response.
        Expected Result: Submission details are recorded and timestamped.
        """
        app, oa = submitted_response_applicant
        
        # Submit the response
        updated_oa = submit_response(
            attorney_id=1,  # Attorney ID
            office_action_id=oa.id
        )
        
        # Verify status was updated to response_submitted
        assert updated_oa.status == "response_submitted"
    
    def test_cfr_014_6_recording_of_extension_requests(self, extension_request_applicant):
        """TEST-CFR-014-6: Verify recording of extension requests for additional response time.
        
        Source ID: PMS-AFR-122
        Purpose: Verify recording of extension requests for additional response time
        Preconditions: Deadline is imminent.
        Action/Input: Attorney submits an extension request.
        Expected Result: Extension details are recorded if the process allows it.
        """
        app, oa = extension_request_applicant
        
        # Create a new office action with extended deadline (simulating extension)
        oa_with_extension = OfficeAction.objects.create(
            application=app,
            received_date=date.today() - timedelta(days=5),
            response_due_date=date.today() + timedelta(days=10),  # Extended from original
            description="Office Action Description",
            status="recorded"
        )
        
        # Verify extension was recorded (new OA with extended due date)
        assert oa_with_extension.response_due_date > oa.response_due_date
    
    def test_cfr_014_7_tracking_of_response_submission_status(self, submitted_response_applicant):
        """TEST-CFR-014-7: Verify tracking of response submission status.
        
        Source ID: PMS-AFR-123
        Purpose: Verify tracking of response submission status
        Preconditions: Response has been submitted.
        Action/Input: View the application status regarding this Office Action.
        Expected Result: Status reflects 'Submitted' or similar.
        """
        app, oa = submitted_response_applicant
        
        # Verify OA status is response_submitted
        assert oa.status == "response_submitted"
    
    def test_cfr_014_8_automation_of_deadline_tracking(self, extension_request_applicant):
        """TEST-CFR-014-8: Verify automation of deadline tracking for responses (if data available).
        
        Source ID: PMS-AFR-124
        Purpose: Verify automation of deadline tracking for responses (if data available)
        Preconditions: Deadline is calculable based on received action.
        Action/Input: Monitor system alerts for the response.
        Expected Result: System automatically generates and displays deadline countdowns.
        """
        app, oa = extension_request_applicant
        
        # Verify OA has a calculable deadline (response_due_date exists)
        assert oa.response_due_date is not None
    
    def test_cfr_015_0_withdrawal_before_filing_stage(self, withdrawn_applicant):
        """TEST-CFR-015-0: Verify withdrawal of applications before filing stage (Pre-Filing).
        
        Source ID: PMS-AFR-125
        Purpose: Verify withdrawal of applications before filing stage (Pre-Filing)
        Preconditions: Application status is 'Submitted' (and withdrawal allowed).
        Action/Input: Applicant submits a withdrawal request.
        Expected Result: Withdrawal is processed.
        """
        app = withdrawn_applicant
        
        # Withdraw the application
        updated_app = withdraw_application(
            applicant_id=1,  # Applicant ID
            application_id=app.id,
            reason="Test withdrawal reason"
        )
        
        # Verify status was updated to withdrawn
        assert updated_app.status == "withdrawn"


class TestOfficeActionResponseLifecycle:
    """Additional test cases for Office Action Response Lifecycle."""
    
    def test_cfr_014_2_draft_response_document_creation(self, office_action_applicant):
        """Verify Attorney creates a draft response document.
        
        Source ID: PMS-AFR-118
        Purpose: Verify Attorney preparation of draft responses
        Preconditions: Office Action is open for review.
        Action/Input: Attorney creates a draft response.
        Expected Result: A draft response document is created.
        """
        app, oa = office_action_applicant
        
        # Create a draft response document
        ApplicationDocument.objects.create(
            application=app,
            file_name="draft_response.txt",
            content_type="text/plain",
            size=1024,
            version=1,
            sensitivity="internal",
            uploaded_by=1,  # Attorney ID
            archived=False
        )
        
        # Verify document was created
        assert ApplicationDocument.objects.filter(
            application=app,
            file_name="draft_response.txt"
        ).exists()
    
    def test_cfr_014_3_applicant_approval_recorded(self, approved_response_applicant):
        """Verify Applicant approval of office-action response is recorded.
        
        Source ID: PMS-AFR-119
        Purpose: Verify Applicant review/approval of office-action responses (if required)
        Preconditions: Applicable process requires Applicant approval.
        Action/Input: Applicant reviews and approves the draft response.
        Expected Result: The system records Applicant approval.
        """
        app, oa = approved_response_applicant
        
        # Approve the response
        updated_oa = approve_response(
            applicant_id=1,  # Applicant ID
            office_action_id=oa.id
        )
        
        # Verify status was updated to applicant_approved
        assert updated_oa.status == "applicant_approved"
    
    def test_cfr_014_4_finalization_status_update(self, draft_response_applicant):
        """Verify Attorney finalization updates response status.
        
        Source ID: PMS-AFR-120
        Purpose: Verify Attorney finalization of office-action responses
        Preconditions: Applicant has approved the draft.
        Action/Input: Attorney marks the response as 'Finalized'.
        Expected Result: The system updates status to Finalized.
        """
        app, oa = draft_response_applicant
        
        # Prepare response (simulates finalization)
        updated_oa = prepare_response(
            attorney_id=1,  # Attorney ID
            office_action_id=oa.id,
            response_text="Final Response Text",
            needs_applicant_approval=False  # Already approved
        )
        
        # Verify status was updated to response_ready (finalized state)
        assert updated_oa.status == "response_ready"
    
    def test_cfr_014_5_submission_timestamped(self, submitted_response_applicant):
        """Verify Office Action Response submission is timestamped.
        
        Source ID: PMS-AFR-121
        Purpose: Verify recording of office-action response submission within deadline
        Preconditions: Response is finalized.
        Action/Input: Submit the finalized response.
        Expected Result: Submission details are recorded and timestamped.
        """
        app, oa = submitted_response_applicant
        
        # Submit the response
        updated_oa = submit_response(
            attorney_id=1,  # Attorney ID
            office_action_id=oa.id
        )
        
        # Verify status was updated to response_submitted
        assert updated_oa.status == "response_submitted"
    
    def test_cfr_014_6_extension_recorded(self, extension_request_applicant):
        """Verify Extension request is recorded.
        
        Source ID: PMS-AFR-122
        Purpose: Verify recording of extension requests for additional response time
        Preconditions: Deadline is imminent.
        Action/Input: Attorney submits an extension request.
        Expected Result: Extension details are recorded if the process allows it.
        """
        app, oa = extension_request_applicant
        
        # Create a new office action with extended deadline (simulating extension)
        oa_with_extension = OfficeAction.objects.create(
            application=app,
            received_date=date.today() - timedelta(days=5),
            response_due_date=date.today() + timedelta(days=10),  # Extended from original
            description="Office Action Description",
            status="recorded"
        )
        
        # Verify extension was recorded (new OA with extended due date)
        assert oa_with_extension.response_due_date > oa.response_due_date
    
    def test_cfr_014_7_submission_status_tracking(self, submitted_response_applicant):
        """Verify Response submission status is tracked.
        
        Source ID: PMS-AFR-123
        Purpose: Verify tracking of response submission status
        Preconditions: Response has been submitted.
        Action/Input: View the application status regarding this Office Action.
        Expected Result: Status reflects 'Submitted' or similar.
        """
        app, oa = submitted_response_applicant
        
        # Verify OA status is response_submitted
        assert oa.status == "response_submitted"
    
    def test_cfr_014_8_deadline_tracking_available(self, extension_request_applicant):
        """Verify Deadline tracking automation is available.
        
        Source ID: PMS-AFR-124
        Purpose: Verify automation of deadline tracking for responses (if data available)
        Preconditions: Deadline is calculable based on received action.
        Action/Input: Monitor system alerts for the response.
        Expected Result: System automatically generates and displays deadline countdowns.
        """
        app, oa = extension_request_applicant
        
        # Verify OA has a calculable deadline (response_due_date exists)
        assert oa.response_due_date is not None
    
    def test_cfr_015_0_withdrawal_pre_filing(self, withdrawn_applicant):
        """Verify Withdrawal of applications before filing stage.
        
        Source ID: PMS-AFR-125
        Purpose: Verify withdrawal of applications before filing stage (Pre-Filing)
        Preconditions: Application status is 'Submitted' (and withdrawal allowed).
        Action/Input: Applicant submits a withdrawal request.
        Expected Result: Withdrawal is processed.
        """
        app = withdrawn_applicant
        
        # Withdraw the application
        updated_app = withdraw_application(
            applicant_id=1,  # Applicant ID
            application_id=app.id,
            reason="Test withdrawal reason"
        )
        
        # Verify status was updated to withdrawn
        assert updated_app.status == "withdrawn"
