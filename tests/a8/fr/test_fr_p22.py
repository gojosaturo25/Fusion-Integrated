"""Tests for notification triggering events - Test Cases 169-176."""
import pytest
from datetime import date, timedelta
from django.test import TestCase
from core.db.mixins import TimeStampedModel

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Budget, Filing, OfficeAction, ApplicationHistory
)
from modules.patent.services.applications import review_application, decide_budget, file_appeal
from modules.patent.services.legal import record_filing
from modules.patent.services.post_filing import record_office_action


@pytest.fixture
def stub_iam(monkeypatch):
    """Fake IAM client for testing."""
    from fusion_auth import client as iam_client
    from fusion_auth.client import IamSession, UserRef
    
    class FakeIam:
        def __init__(self, session=None, users=None):
            self.session = session
            self.users = users or {}
        
        def login(self, username, password):
            return "tok-123"
    
    fake = FakeIam()
    patched = 0
    for mod in list(monkeypatch.list):
        if getattr(mod, "__name__", "") == "fusion_auth.client":
            monkeypatch.setattr(iam_client, "get_client", lambda: fake)
            patched += 1
    
    return fake


@pytest.fixture
def user_ref():
    """Create a test user reference."""
    def _make(user_id, name="Test User", kind="student"):
        return UserRef(user_id=user_id, username=f"u{user_id}", display_name=name,
                       kind=kind)
    return _make


@pytest.fixture
def principal(applicant_id=1001):
    """Create a test principal."""
    from conftest import make_principal
    return make_principal(user_id=applicant_id, kind="student")


@pytest.fixture
def application(principal):
    """Create a test patent application."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-001",
        applicant_id=principal.user_id,
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Technology",
        status="submitted"
    )
    return app


@pytest.fixture
def director_principal(applicant_id=1002):
    """Create a test director principal."""
    from conftest import make_principal
    return make_principal(user_id=applicant_id, kind="director")


@pytest.fixture
def budget(application):
    """Create a test budget."""
    budget = Budget.objects.create(
        application=application,
        filing_fee=1000.00,
        attorney_fee=500.00,
        administrative_cost=200.00,
        total=1700.00,
        status="pending"
    )
    return budget


@pytest.fixture
def filing(application):
    """Create a test filing."""
    filing = Filing.objects.create(
        application=application,
        patent_office="USPTO",
        filing_number="12345678",
        filing_date=date.today(),
        international=False
    )
    return filing


@pytest.fixture
def office_action(application):
    """Create a test office action."""
    oa = OfficeAction.objects.create(
        application=application,
        received_date=date.today(),
        response_due_date=date.today() + timedelta(days=30),
        description="Office Action Description",
        status="recorded"
    )
    return oa


@pytest.fixture
def document(application):
    """Create a test document."""
    from modules.patent.models import ApplicationDocument
    doc = ApplicationDocument.objects.create(
        application=application,
        file_name="test.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity="internal",
        uploaded_by=application.applicant_id
    )
    return doc


@pytest.fixture
def notification_log():
    """Mock notification log for testing."""
    class NotificationLog:
        def __init__(self):
            self.entries = []
        
        def add(self, event_type, recipient, message):
            self.entries.append({
                "event_type": event_type,
                "recipient": recipient,
                "message": message
            })
        
        def get_entries(self):
            return self.entries
        
        def __len__(self):
            return len(self.entries)
    
    return NotificationLog()


@pytest.fixture
def email_log_checker(notification_log):
    """Helper to check notification logs."""
    
    def get_logs():
        return notification_log.get_entries()
    
    return get_logs


class TestNotificationTriggeringEvents:
    """Test cases for notification triggering events (TEST-CFR-023-4 through TEST-CFR-023-11)."""

    @pytest.mark.django_db
    def test_cfr_023_4_notification_for_review_decisions(self, application, director_principal):
        """TEST-CFR-023-4: Verification of triggering notification for review decisions.
        
        Source ID: PMS-AFR-196
        Purpose: Verify that email notifications are triggered when a Director makes a review decision.
        Preconditions: Decision is made.
        Action/Input: Check email logs.
        Expected Result: Notification is triggered.
        """
        # Arrange
        director_id = director_principal.user_id
        
        # Act - Make a review decision
        review_application(
            director_id=director_id,
            application_id=application.id,
            decision="approve",
            justification="This application meets all patentability criteria." * 2
        )
        
        # Assert - Check email logs
        assert len(email_log_checker()) > 0, "Email notification should be triggered for review decision"

    @pytest.mark.django_db
    def test_cfr_023_5_notification_for_budget_approval_rejection(self, application, director_principal):
        """TEST-CFR-023-5: Verification of triggering notification for budget approval/rejection.
        
        Source ID: PMS-AFR-197
        Purpose: Verify that email notifications are triggered when a Director makes a budget decision.
        Preconditions: Budget decision is made.
        Action/Input: Check email logs.
        Expected Result: Notification is triggered.
        """
        # Arrange
        director_id = director_principal.user_id
        
        # Act - Make a budget decision (approve)
        decide_budget(
            director_id=director_id,
            budget_id=budget.id,
            approve=True,
            justification="Budget approved for patent filing." * 2
        )
        
        # Assert - Check email logs
        assert len(email_log_checker()) > 0, "Email notification should be triggered for budget decision"

    @pytest.mark.django_db
    def test_cfr_023_6_notification_for_filing_confirmations(self, application, director_principal):
        """TEST-CFR-023-6: Verification of triggering notification for filing confirmations.
        
        Source ID: PMS-AFR-198
        Purpose: Verify that email notifications are triggered when a patent filing is recorded.
        Preconditions: Filing is recorded.
        Action/Input: Check email logs.
        Expected Result: Notification is triggered.
        """
        # Arrange
        attorney_id = director_principal.user_id
        
        # Act - Record a filing
        record_filing(
            attorney_id=attorney_id,
            application_id=application.id,
            office="USPTO",
            filing_number="12345678",
            filing_date=date.today(),
            international=False
        )
        
        # Assert - Check email logs
        assert len(email_log_checker()) > 0, "Email notification should be triggered for filing confirmation"

    @pytest.mark.django_db
    def test_cfr_023_7_notification_for_office_actions(self, application, director_principal):
        """TEST-CFR-023-7: Verification of triggering notification for office actions.
        
        Source ID: PMS-AFR-199
        Purpose: Verify that email notifications are triggered when an Office Action is recorded.
        Preconditions: Office Action recorded.
        Action/Input: Check email logs.
        Expected Result: Notification is triggered.
        """
        # Arrange
        attorney_id = director_principal.user_id
        
        # Act - Record an office action
        record_office_action(
            attorney_id=attorney_id,
            application_id=application.id,
            received_date=date.today(),
            response_due_date=date.today() + timedelta(days=30),
            description="Office Action Description"
        )
        
        # Assert - Check email logs
        assert len(email_log_checker()) > 0, "Email notification should be triggered for office action"

    @pytest.mark.django_db
    def test_cfr_023_8_notification_for_deadline_reminders(self, application, director_principal):
        """TEST-CFR-023-8: Verification of triggering notification for deadline reminders.
        
        Source ID: PMS-AFR-200
        Purpose: Verify that email notifications are triggered when a deadline is approaching.
        Preconditions: Deadline approaching.
        Action/Input: Check email logs.
        Expected Result: Notification is triggered.
        """
        # Arrange - Set up application with near deadline
        from datetime import timedelta
        
        # Act - Simulate deadline reminder (via review decision that sets deadline)
        review_application(
            director_id=director_principal.user_id,
            application_id=application.id,
            decision="needs_revision",
            justification="Application needs revision to meet patentability standards." * 2
        )
        
        # Assert - Check email logs (deadline reminder should be triggered)
        assert len(email_log_checker()) > 0, "Email notification should be triggered for deadline reminder"

    @pytest.mark.django_db
    def test_cfr_023_9_notification_for_deadline_escalations(self, application, director_principal):
        """TEST-CFR-023-9: Verification of triggering notification for deadline escalations.
        
        Source ID: PMS-AFR-201
        Purpose: Verify that email notifications are triggered when a deadline is missed and escalated.
        Preconditions: Deadline missed.
        Action/Input: Check email logs.
        Expected Result: Notification is triggered.
        """
        # Arrange - Set up application with past deadline
        from datetime import timedelta
        
        # Act - Simulate escalation (via system auto-expire or manual escalation)
        # This would typically be handled by a background task, but we simulate the notification trigger
        expired_apps = []
        from modules.patent.services.applications import expire_overdue_resubmissions
        
        today = date.today()
        expired_apps = expire_overdue_resubmissions(today)
        
        # Assert - Check email logs (escalation notification should be triggered)
        assert len(email_log_checker()) > 0, "Email notification should be triggered for deadline escalation"

    @pytest.mark.django_db
    def test_cfr_023_10_notification_for_maintenance_fee_reminders(self, application, director_principal):
        """TEST-CFR-023-10: Verification of triggering notification for maintenance fee reminders.
        
        Source ID: PMS-AFR-202
        Purpose: Verify that email notifications are triggered when a maintenance fee is due.
        Preconditions: Maintenance due.
        Action/Input: Check email logs.
        Expected Result: Notification is triggered.
        """
        # Arrange - Set up granted application with maintenance record
        from datetime import timedelta
        
        # Act - Schedule maintenance and simulate reminder trigger
        from modules.patent.services.post_filing import schedule_maintenance
        
        attorney_id = director_principal.user_id
        due_date = date.today() - timedelta(days=10)  # Already due
        
        schedule_maintenance(
            attorney_id=attorney_id,
            application_id=application.id,
            due_date=due_date,
            fee=500.00
        )
        
        # Assert - Check email logs (maintenance reminder should be triggered)
        assert len(email_log_checker()) > 0, "Email notification should be triggered for maintenance fee reminder"

    @pytest.mark.django_db
    def test_cfr_023_11_notification_for_document_updates(self, application, director_principal):
        """TEST-CFR-023-11: Verification of triggering notification for document updates.
        
        Source ID: PMS-AFR-203
        Purpose: Verify that email notifications are triggered when a document is updated.
        Preconditions: Document updated.
        Action/Input: Check email logs.
        Expected Result: Notification is triggered.
        """
        # Arrange - Create initial document
        
        # Act - Update the document (simulated via service)
        from modules.patent.models import ApplicationDocument
        
        doc = ApplicationDocument.objects.create(
            application=application,
            file_name="test.pdf",
            content_type="application/pdf",
            size=102400,
            version=1,
            sensitivity="internal",
            uploaded_by=application.applicant_id
        )
        
        # Simulate document update (in real system, this would be via a service)
        doc.version += 1
        doc.size = 204800  # Updated size
        doc.save()
        
        # Assert - Check email logs (document update notification should be triggered)
        assert len(email_log_checker()) > 0, "Email notification should be triggered for document update"
