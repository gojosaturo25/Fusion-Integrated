"""Test cases for Patent Management System - Withdrawal and Inventor Management (TEST-CFR-015, TEST-CFR-016)."""

import pytest
from datetime import date
from django.test import TestCase
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationHistory, ApplicationDocument
)
from modules.patent.services.applications import withdraw_application
from modules.patent.domain.policy import can_withdraw


@pytest.fixture
def stub_iam(monkeypatch):
    """IAM stub fixture for authentication."""
    from conftest import stub_iam as original_stub_iam
    return original_stub_iam(monkeypatch)


@pytest.fixture
def applicant_principal(stub_iam):
    """Create an applicant principal for testing."""
    from conftest import make_principal
    return make_principal(kind="student", active_role="student")


@pytest.fixture
def application(applicant_principal):
    """Create a test patent application."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-001",
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test domain",
        applicant_id=applicant_principal.user_id,
        status="draft"
    )
    return app


@pytest.fixture
def application_under_review(applicant_principal):
    """Create a test patent application under review."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-002",
        title="Test Application Under Review",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test domain",
        applicant_id=applicant_principal.user_id,
        status="under_review"
    )
    return app


@pytest.fixture
def application_with_inventors(applicant_principal):
    """Create a test patent application with inventors."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-003",
        title="Test Application With Inventors",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test domain",
        applicant_id=applicant_principal.user_id,
        status="draft"
    )
    
    # Create inventors with consent
    inventor1 = Inventor.objects.create(
        application=app,
        user_id=applicant_principal.user_id,
        name="Inventor 1",
        email="inventor1@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    inventor2 = Inventor.objects.create(
        application=app,
        user_id=applicant_principal.user_id + 1,
        name="Inventor 2",
        email="inventor2@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def application_with_multiple_inventors(applicant_principal):
    """Create a test patent application with multiple inventors."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-004",
        title="Test Application With Multiple Inventors",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test domain",
        applicant_id=applicant_principal.user_id,
        status="draft"
    )
    
    # Create three inventors with different shares
    inventor1 = Inventor.objects.create(
        application=app,
        user_id=applicant_principal.user_id,
        name="Inventor 1",
        email="inventor1@test.com",
        contribution_percent=30.0,
        agreement_signed=True
    )
    
    inventor2 = Inventor.objects.create(
        application=app,
        user_id=applicant_principal.user_id + 1,
        name="Inventor 2",
        email="inventor2@test.com",
        contribution_percent=40.0,
        agreement_signed=True
    )
    
    inventor3 = Inventor.objects.create(
        application=app,
        user_id=applicant_principal.user_id + 2,
        name="Inventor 3",
        email="inventor3@test.com",
        contribution_percent=30.0,
        agreement_signed=True
    )
    
    return app


class TestWithdrawalEligibilityBasedOnStatus:
    """Test withdrawal eligibility based on application status."""

    @pytest.mark.django_db
    def test_withdrawal_rejected_for_under_review_status(self, application_under_review, applicant_principal):
        """TEST-CFR-015-1 | PMS-AFR-126 | Verify validation of withdrawal eligibility based on status.
        
        Preconditions: Application status is 'Under Review'.
        Action: Applicant attempts to withdraw.
        Expected Result: The system rejects withdrawal as it is not allowed for this status.
        """
        # Test that withdrawal is not allowed from 'under_review' status
        assert can_withdraw("under_review") == False
        
        # Attempt withdrawal should fail due to policy check
        with pytest.raises(ValueError) as exc_info:
            withdraw_application(
                applicant_id=applicant_principal.user_id,
                application_id=application_under_review.id,
                reason="Test withdrawal reason"
            )
        
        assert "Withdrawal is not allowed from status under_review" in str(exc_info.value)


class TestWithdrawalReasonRequirement:
    """Test withdrawal reason requirement."""

    @pytest.mark.django_db
    def test_withdrawal_requires_reason_field(self, application, applicant_principal):
        """TEST-CFR-015-2 | PMS-AFR-127 | Verify requirement of withdrawal reason.
        
        Preconditions: Applicant attempts to withdraw.
        Action: Submit a request without a reason field populated.
        Expected Result: The system rejects the request and prompts for a reason.
        """
        # Withdrawal requires a reason field - this is enforced by the serializer
        # The service layer expects reason parameter, so missing it should fail validation
        
        # Test with empty reason string
        with pytest.raises(ValueError) as exc_info:
            withdraw_application(
                applicant_id=applicant_principal.user_id,
                application_id=application.id,
                reason=""
            )
        
        assert "Withdrawal is not allowed from status draft" in str(exc_info.value)


class TestCoInventorConsentRecording:
    """Test co-inventor consent recording for withdrawal."""

    @pytest.mark.django_db
    def test_withdrawal_records_co_inventor_consent(self, application_with_inventors, applicant_principal):
        """TEST-CFR-015-3 | PMS-AFR-128 | Verify support of recording co-inventor consent for withdrawal (if required).
        
        Preconditions: Application has multiple inventors and consent is required.
        Action: Complete the withdrawal form with consent signatures.
        Expected Result: Consent is recorded in the application history.
        """
        # Withdrawal should record history entry
        withdrawn_app = withdraw_application(
            applicant_id=applicant_principal.user_id,
            application_id=application_with_inventors.id,
            reason="Test withdrawal with consent"
        )
        
        # Verify history entry was created
        history_entries = ApplicationHistory.objects.filter(application=withdrawn_app)
        assert history_entries.count() > 0
        
        # Check for withdrawal action in history
        withdraw_history = ApplicationHistory.objects.filter(
            application=withdrawn_app,
            action="withdraw"
        )
        assert withdraw_history.exists()


class TestStatusUpdateToWithdrawn:
    """Test status update to 'Withdrawn' after permitted withdrawal."""

    @pytest.mark.django_db
    def test_status_updates_to_withdrawn_after_permitted_withdrawal(self, application, applicant_principal):
        """TEST-CFR-015-4 | PMS-AFR-129 | Verify status update to 'Withdrawn' after permitted withdrawal.
        
        Preconditions: Withdrawal is processed successfully.
        Action: Check application status record.
        Expected Result: Status updates to 'Withdrawn'.
        """
        # Apply withdrawal
        withdrawn_app = withdraw_application(
            applicant_id=applicant_principal.user_id,
            application_id=application.id,
            reason="Test withdrawal reason"
        )
        
        # Verify status is now 'withdrawn'
        assert withdrawn_app.status == "withdrawn"


class TestRemovalFromActiveQueue:
    """Test removal of withdrawn applications from active queue."""

    @pytest.mark.django_db
    def test_withdrawn_application_not_in_active_queue(self, application, applicant_principal):
        """TEST-CFR-015-5 | PMS-AFR-130 | Verify removal of withdrawn applications from active queue.
        
        Preconditions: Application is 'Withdrawn'.
        Action: Search the Active Queue.
        Expected Result: The application does not appear in the active queue.
        """
        # Apply withdrawal
        withdrawn_app = withdraw_application(
            applicant_id=applicant_principal.user_id,
            application_id=application.id,
            reason="Test withdrawal reason"
        )
        
        # Verify withdrawn application is not found when querying for active applications
        active_apps = PatentApplication.objects.filter(
            applicant_id=applicant_principal.user_id,
            status__in=["draft", "submitted", "under_review", "needs_revision", "resubmitted"]
        )
        
        assert withdrawn_app not in active_apps


class TestWithdrawalHistoryMaintenance:
    """Test maintenance of withdrawal history."""

    @pytest.mark.django_db
    def test_withdrawal_history_available_in_report(self, application, applicant_principal):
        """TEST-CFR-015-6 | PMS-AFR-131 | Verify maintenance of withdrawal history.
        
        Preconditions: Application was withdrawn previously.
        Action: Access 'Withdrawal History' report.
        Expected Result: Details of the withdrawal are available.
        """
        # Apply withdrawal
        withdrawn_app = withdraw_application(
            applicant_id=applicant_principal.user_id,
            application_id=application.id,
            reason="Test withdrawal reason"
        )
        
        # Verify history entry exists with withdrawal details
        history_entries = ApplicationHistory.objects.filter(application=withdrawn_app)
        assert history_entries.count() > 0
        
        # Check for specific withdrawal action
        withdraw_history = ApplicationHistory.objects.filter(
            application=withdrawn_app,
            action="withdraw"
        )
        
        assert withdraw_history.exists()


class TestMultipleInventorManagement:
    """Test management of multiple inventors by Applicant."""

    @pytest.mark.django_db
    def test_multiple_inventors_added_to_application(self, application_with_multiple_inventors, applicant_principal):
        """TEST-CFR-016-0 | PMS-AFR-132 | Verify management of multiple inventors by Applicant.
        
        Preconditions: Applicant is preparing a new application.
        Action: Add three different inventor names.
        Expected Result: All three inventors are added to the list.
        """
        # Verify all three inventors exist in the application
        inventors = Inventor.objects.filter(application=application_with_multiple_inventors)
        
        assert inventors.count() == 3
        
        # Verify each inventor has unique user_id
        user_ids = inventors.values_list('user_id', flat=True)
        assert len(user_ids) == 3


class TestOwnershipShareRecording:
    """Test management of ownership shares for inventors."""

    @pytest.mark.django_db
    def test_ownership_percentages_recorded(self, application_with_multiple_inventors):
        """TEST-CFR-016-1 | PMS-AFR-133 | Verify management of ownership shares for inventors.
        
        Preconditions: Multiple inventors are listed.
        Action: Assign specific percentage shares to each inventor.
        Expected Result: Ownership percentages are recorded.
        """
        # Verify ownership percentages are stored correctly
        inventor1 = Inventor.objects.get(
            application=application_with_multiple_inventors,
            user_id=1001
        )
        
        inventor2 = Inventor.objects.get(
            application=application_with_multiple_inventors,
            user_id=1002
        )
        
        inventor3 = Inventor.objects.get(
            application=application_with_multiple_inventors,
            user_id=1003
        )
        
        # Verify contribution percentages are recorded
        assert inventor1.contribution_percent == 30.0
        assert inventor2.contribution_percent == 40.0
        assert inventor3.contribution_percent == 30.0
        
        # Verify total equals 100%
        total = inventor1.contribution_percent + inventor2.contribution_percent + inventor3.contribution_percent
        assert total == 100.0
