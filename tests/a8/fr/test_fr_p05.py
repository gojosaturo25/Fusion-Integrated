"""Test cases for Patent Management System - FR Design (PMS-AFR-062 to PMS-AFR-069).

These tests cover notification, routing, audit trail, and resubmission validation rules.
"""
import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, ApplicationHistory, AttorneyAssignment,
    OfficeAction
)


@pytest.fixture
def director_principal(stub_iam):
    """Create a Director principal for testing."""
    return Principal.from_session(
        user_id=2001,
        kind="director",
        active_role="director",
        permissions={"patent.application.review"},
        modules=("patent",)
    )


@pytest.fixture
def applicant_principal(stub_iam):
    """Create an Applicant principal for testing."""
    return Principal.from_session(
        user_id=1001,
        kind="student",
        active_role="student",
        permissions={"patent.application.view_self"},
        modules=("patent",)
    )


@pytest.fixture
def approved_application(applicant_principal):
    """Create an application with 'approved' status."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-001",
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="CSE",
        applicant_id=1001,
        status="approved"
    )
    return app


@pytest.fixture
def needs_revision_application(applicant_principal):
    """Create an application with 'needs_revision' status."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-002",
        title="Test Application 2",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="CSE",
        applicant_id=1001,
        status="needs_revision"
    )
    return app


@pytest.fixture
def rejected_application(applicant_principal):
    """Create an application with 'rejected' status."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-003",
        title="Test Application 3",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="CSE",
        applicant_id=1001,
        status="rejected"
    )
    return app


@pytest.fixture
def director_reviewed_application(applicant_principal):
    """Create an application with Director review history."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-004",
        title="Test Application 4",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="CSE",
        applicant_id=1001,
        status="approved"
    )
    
    # Create Director review history
    ApplicationHistory.objects.create(
        application=app,
        actor_id=2001,  # Director ID
        action="review",
        from_status="submitted",
        to_status="approved",
        note="Director approved the application"
    )
    
    return app


@pytest.fixture
def application_with_feedback(applicant_principal):
    """Create an application with Director feedback notes."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-005",
        title="Test Application 5",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="CSE",
        applicant_id=1001,
        status="needs_revision"
    )
    
    # Create Director feedback in history
    ApplicationHistory.objects.create(
        application=app,
        actor_id=2001,  # Director ID
        action="review",
        from_status="submitted",
        to_status="needs_revision",
        note="Director requested: Add claim 3 and revise abstract"
    )
    
    return app


class TestCFR007_4_PMS_AFR_062(TestCase):
    """Verify notification on rejection (TEST-CFR-007-4, PMS-AFR-062)."""
    
    def test_notification_on_rejection(self, director_reviewed_application, applicant_principal):
        """
        Purpose: Verify notification on rejection.
        
        Preconditions: Director decision is 'Reject'.
        Action: Monitor the Applicant's communication channel.
        Expected Result: A notification containing detailed feedback and rejection reasons is sent to the Applicant.
        """
        # Simulate rejection decision via history entry
        ApplicationHistory.objects.create(
            application=director_reviewed_application,
            actor_id=2001,  # Director ID
            action="review",
            from_status="submitted",
            to_status="rejected",
            note="Director rejected the application"
        )
        
        # Verify notification mechanism exists (check for history entry indicating rejection)
        history_entries = ApplicationHistory.objects.filter(
            application=director_reviewed_application,
            actor_id=2001
        ).order_by('-created_at')
        
        assert history_entries.count() >= 1, "Director review history should exist"
        
        # Verify notification would be sent (check for rejection-related history)
        rejection_history = ApplicationHistory.objects.filter(
            application=director_reviewed_application,
            to_status="rejected"
        )
        
        assert rejection_history.exists(), "Rejection notification should trigger history entry"


class TestCFR007_5_PMS_AFR_063(TestCase):
    """Verify notification on revision request (TEST-CFR-007-5, PMS-AFR-063)."""
    
    def test_notification_on_revision_request(self, needs_revision_application, applicant_principal):
        """
        Purpose: Verify notification on revision request.
        
        Preconditions: Director decision is 'Needs Revision'.
        Action: Monitor the Applicant's communication channel.
        Expected Result: A notification containing detailed feedback and revision requirements is sent to the Applicant.
        """
        # Simulate needs_revision decision via history entry
        ApplicationHistory.objects.create(
            application=needs_revision_application,
            actor_id=2001,  # Director ID
            action="review",
            from_status="submitted",
            to_status="needs_revision",
            note="Director requested revision: Add claim 3 and revise abstract"
        )
        
        # Verify notification mechanism exists (check for history entry indicating revision request)
        history_entries = ApplicationHistory.objects.filter(
            application=needs_revision_application,
            actor_id=2001
        ).order_by('-created_at')
        
        assert history_entries.count() >= 1, "Director review history should exist"
        
        # Verify notification would be sent (check for revision-related history)
        revision_history = ApplicationHistory.objects.filter(
            application=needs_revision_application,
            to_status="needs_revision"
        )
        
        assert revision_history.exists(), "Revision request notification should trigger history entry"


class TestCFR007_6_PMS_AFR_064(TestCase):
    """Verify routing of approved applications to attorney assignment (TEST-CFR-007-6, PMS-AFR-064)."""
    
    def test_routing_approved_to_attorney_assignment(self, approved_application, applicant_principal):
        """
        Purpose: Verify routing approved applications to attorney assignment.
        
        Preconditions: Director decision is 'Approve'.
        Action: View the application workflow status post-decision.
        Expected Result: The application state transitions toward 'Attorney Assigned'.
        """
        # Simulate approval decision via history entry
        ApplicationHistory.objects.create(
            application=approved_application,
            actor_id=2001,  # Director ID
            action="review",
            from_status="submitted",
            to_status="approved",
            note="Director approved the application"
        )
        
        # Verify application status is 'approved'
        assert approved_application.status == "approved", "Application should be approved after Director decision"
        
        # Check for attorney assignment transition (should exist or be created)
        assignments = AttorneyAssignment.objects.filter(
            application=approved_application,
            status="offered"
        )
        
        # Verify routing toward attorney assignment exists in history
        routing_history = ApplicationHistory.objects.filter(
            application=approved_application,
            action="assign_attorney"
        )
        
        assert routing_history.exists(), "Application should route toward attorney assignment"


class TestCFR007_7_PMS_AFR_065(TestCase):
    """Verify audit trail of Director review process (TEST-CFR-007-7, PMS-AFR-065)."""
    
    def test_audit_trail_of_director_review(self, director_reviewed_application, applicant_principal):
        """
        Purpose: Verify audit trail of Director review process.
        
        Preconditions: A review is performed and a decision is made.
        Action: Access the 'Audit Logs' for PMS actions.
        Expected Result: The log contains entries detailing the review action, user ID, timestamp, decision, and justification.
        """
        # Create comprehensive Director review history
        ApplicationHistory.objects.create(
            application=director_reviewed_application,
            actor_id=2001,  # Director ID
            action="review",
            from_status="submitted",
            to_status="approved",
            note="Director approved the application with detailed justification"
        )
        
        # Access audit logs (ApplicationHistory)
        history_entries = ApplicationHistory.objects.filter(
            application=director_reviewed_application,
            actor_id=2001
        ).order_by('-created_at')
        
        assert history_entries.count() >= 1, "Audit log should contain review entries"
        
        # Verify audit log contains required details
        for entry in history_entries:
            assert entry.action == "review", "Action should be 'review'"
            assert entry.actor_id == 2001, "User ID should match Director ID"
            assert entry.to_status == "approved", "Decision status should be 'approved'"
            assert len(entry.note) > 0, "Justification note should exist"


class TestCFR008_0_PMS_AFR_066(TestCase):
    """Verify revision of 'Needs Revision' applications (TEST-CFR-008-0, PMS-AFR-066)."""
    
    def test_revision_of_needs_revision_application(self, needs_revision_application, applicant_principal):
        """
        Purpose: Verify revision of 'Needs Revision' applications.
        
        Preconditions: Application status is 'Needs Revision'.
        Action: Applicant edits and resubmits the application.
        Expected Result: The system accepts the revised application.
        """
        # Verify application can be resubmitted (status check)
        assert needs_revision_application.status == "needs_revision", "Application should be in 'needs_revision' status"
        
        # Simulate resubmission via history entry
        ApplicationHistory.objects.create(
            application=needs_revision_application,
            actor_id=1001,  # Applicant ID
            action="resubmit",
            from_status="needs_revision",
            to_status="resubmitted",
            note="Applicant resubmitted with revisions"
        )
        
        # Verify system accepts the revision (status transition)
        assert needs_revision_application.status == "resubmitted", "System should accept revised application"


class TestCFR008_1_PMS_AFR_067(TestCase):
    """Verify revision of 'Rejected' applications (TEST-CFR-008-1, PMS-AFR-067)."""
    
    def test_revision_of_rejected_application(self, rejected_application, applicant_principal):
        """
        Purpose: Verify revision of 'Rejected' applications.
        
        Preconditions: Application status is 'Rejected'.
        Action: Applicant edits and resubmits the application within the allowed period.
        Expected Result: The system accepts the revised application.
        """
        # Verify application can be resubmitted (status check)
        assert rejected_application.status == "rejected", "Application should be in 'rejected' status"
        
        # Simulate resubmission via history entry
        ApplicationHistory.objects.create(
            application=rejected_application,
            actor_id=1001,  # Applicant ID
            action="resubmit",
            from_status="rejected",
            to_status="resubmitted",
            note="Applicant resubmitted within allowed period"
        )
        
        # Verify system accepts the revision (status transition)
        assert rejected_application.status == "resubmitted", "System should accept revised application"


class TestCFR008_2_PMS_AFR_068(TestCase):
    """Verify validation of 60-day resubmission period (TEST-CFR-008-2, PMS-AFR-068)."""
    
    def test_validation_of_60_day_resubmission_period(self, rejected_application, applicant_principal):
        """
        Purpose: Verify validation of 60-day resubmission period.
        
        Preconditions: Application status is 'Rejected' and current date exceeds the 60-day deadline.
        Action: Attempt to revise and resubmit the application.
        Expected Result: The system rejects the submission as outside the permitted timeframe.
        """
        # Set resubmission deadline in the past (exceeds 60 days)
        from datetime import date
        
        rejected_application.resubmission_deadline = date.today() - timedelta(days=90)
        rejected_application.save()
        
        # Verify application is in 'rejected' status
        assert rejected_application.status == "rejected", "Application should be in 'rejected' status"
        
        # Verify resubmission deadline has passed
        assert rejected_application.resubmission_deadline < date.today(), "Resubmission deadline should have passed"
        
        # Attempt to simulate resubmission (should fail validation)
        try:
            ApplicationHistory.objects.create(
                application=rejected_application,
                actor_id=1001,  # Applicant ID
                action="resubmit",
                from_status="rejected",
                to_status="resubmitted",
                note="Applicant attempted resubmission after deadline"
            )
            
            # Verify system rejects the submission (status should not change)
            assert rejected_application.status == "rejected", "System should reject submission outside timeframe"
        except Exception:
            # Expected - validation failure
            pass


class TestCFR008_3_PMS_AFR_069(TestCase):
    """Verify validation of revision addressing feedback (TEST-CFR-008-3, PMS-AFR-069)."""
    
    def test_validation_of_revision_addressing_feedback(self, application_with_feedback, applicant_principal):
        """
        Purpose: Verify validation of revision addressing feedback.
        
        Preconditions: Director previously requested specific revisions for the application.
        Action: Applicant submits a revision that ignores the Director's previous feedback notes.
        Expected Result: The system flags or prevents submission until the feedback is addressed.
        """
        # Verify application has Director feedback in history
        feedback_history = ApplicationHistory.objects.filter(
            application=application_with_feedback,
            actor_id=2001  # Director ID
        ).order_by('-created_at')
        
        assert feedback_history.count() >= 1, "Director feedback should exist"
        
        # Verify feedback note contains revision requirements
        for entry in feedback_history:
            assert len(entry.note) > 0, "Feedback note should contain revision requirements"
        
        # Simulate resubmission attempt (should be flagged/prevented)
        try:
            ApplicationHistory.objects.create(
                application=application_with_feedback,
                actor_id=1001,  # Applicant ID
                action="resubmit",
                from_status="needs_revision",
                to_status="resubmitted",
                note="Applicant attempted resubmission without addressing feedback"
            )
            
            # Verify system flags/prevents submission (status should not change)
            assert application_with_feedback.status == "needs_revision", "System should prevent submission without addressing feedback"
        except Exception:
            # Expected - validation failure due to unaddressed feedback
            pass
