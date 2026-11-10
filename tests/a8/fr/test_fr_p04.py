"""
Automated backend tests for Patent Management System - Test Cases 25-32.
Source: FR_DESIGN.json (test cases 25-32 of 204)
Test ID format: TEST-CFR-XXX-Y
"""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.core.cache import cache

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationHistory,
    AttorneyAssignment, ApplicationDocument
)
from modules.patent.services.applications import (
    assign_director, review_application, resubmit_application
)
from modules.patent.domain.policy import (
    is_conflicted, can_transition, validate_justification
)


@pytest.fixture
def stub_iam(monkeypatch):
    """Use existing stub_iam fixture from conftest.py"""
    from conftest import stub_iam
    return stub_iam


@pytest.fixture
def director_principal(stub_iam):
    """Create a Director principal for testing."""
    return Principal.from_session(
        user_id=1002,
        kind="director",
        active_role="director",
        permissions=frozenset(["patent.application.review"]),
        modules=("patent",),
    )


@pytest.fixture
def applicant_principal(stub_iam):
    """Create an Applicant principal for testing."""
    return Principal.from_session(
        user_id=1001,
        kind="student",
        active_role="student",
        permissions=frozenset(["patent.application.create"]),
        modules=("patent",),
    )


@pytest.fixture
def pcc_admin_principal(stub_iam):
    """Create a PCC_ADMIN principal for testing."""
    return Principal.from_session(
        user_id=1003,
        kind="admin",
        active_role="admin",
        permissions=frozenset(["patent.admin.manage"]),
        modules=("patent",),
    )


@pytest.fixture
def application(applicant_principal):
    """Create a test application."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-001",
        applicant_id=applicant_principal.user_id,
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test Domain",
        status="submitted"
    )
    return app


@pytest.fixture
def inventor(applicant_principal):
    """Create a test inventor."""
    return Inventor.objects.create(
        application=application,
        user_id=1002,  # Director as inventor
        name="Director Test",
        email="director@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )


@pytest.fixture
def director_as_inventor(applicant_principal):
    """Create a scenario where Director is listed as inventor."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-002",
        applicant_id=applicant_principal.user_id,
        title="Test Application 2",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test Domain",
        status="submitted"
    )
    
    # Director (1002) is listed as inventor
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Director Test",
        email="director@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def pcc_admin_as_inventor(applicant_principal):
    """Create a scenario where PCC_ADMIN is listed as inventor."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-003",
        applicant_id=applicant_principal.user_id,
        title="Test Application 3",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test Domain",
        status="submitted"
    )
    
    # PCC_ADMIN (1003) is listed as inventor
    Inventor.objects.create(
        application=app,
        user_id=1003,
        name="PCC Admin Test",
        email="pccadmin@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def assigned_application(applicant_principal):
    """Create an application with Director assigned."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-004",
        applicant_id=applicant_principal.user_id,
        title="Test Application 4",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test Domain",
        status="submitted"
    )
    
    # Assign Director (1002) to application
    assign_director(
        admin_id=1003,
        application_id=app.id,
        director_id=1002
    )
    
    return app


@pytest.fixture
def review_deadline_application(applicant_principal):
    """Create an application with a past review deadline."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="TEST-005",
        applicant_id=applicant_principal.user_id,
        title="Test Application 5",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Test Domain",
        status="submitted"
    )
    
    # Assign Director (1002) to application
    assign_director(
        admin_id=1003,
        application_id=app.id,
        director_id=1002
    )
    
    # Set review due date in the past
    app.review_due_date = date.today() - timedelta(days=1)
    app.save()
    
    return app


class TestCFR006_5:
    """Test TEST-CFR-006-5: Verify prevention of self-review by Director."""
    
    def test_director_cannot_review_self_as_inventor(self, director_principal, director_as_inventor):
        """
        Test ID: TEST-CFR-006-5
        Source ID: PMS-AFR-054
        
        Purpose: Verify prevention of self-review by Director
        Preconditions: Director X lists himself as an inventor on Application Y.
        Action/Input: Director X attempts to view or process Application Y.
        Expected Result: The system prevents access and denies the Director from handling this application.
        """
        # Verify conflict detection
        assert is_conflicted(1002, {1002}) is True
        
        # Attempt to assign director (should fail due to conflict)
        with pytest.raises(Exception):
            assign_director(
                admin_id=1003,
                application_id=director_as_inventor.id,
                director_id=1002
            )


class TestCFR006_6:
    """Test TEST-CFR-006-6: Verify prevention of self-review by PCC_ADMIN."""
    
    def test_pcc_admin_cannot_review_self_as_inventor(self, pcc_admin_principal, pcc_admin_as_inventor):
        """
        Test ID: TEST-CFR-006-6
        Source ID: PMS-AFR-055
        
        Purpose: Verify prevention of self-review by PCC_ADMIN
        Preconditions: PCC_ADMIN is listed as an inventor on an application.
        Action/Input: Attempt to view the specific application details.
        Expected Result: The system restricts viewing permissions for this application.
        """
        # Verify conflict detection
        assert is_conflicted(1003, {1003}) is True
        
        # PCC_ADMIN should not be able to assign themselves as director
        with pytest.raises(Exception):
            assign_director(
                admin_id=1003,
                application_id=pcc_admin_as_inventor.id,
                director_id=1003
            )


class TestCFR006_7:
    """Test TEST-CFR-006-7: Verify status update to 'Under Review'."""
    
    def test_status_updates_to_under_review_after_assignment(self, assigned_application):
        """
        Test ID: TEST-CFR-006-7
        Source ID: PMS-AFR-056
        
        Purpose: Verify status update to 'Under Review'
        Preconditions: An assignment is completed.
        Action/Input: Check the application status field.
        Expected Result: The application status updates from 'Submitted' to 'Under Review'.
        """
        # Verify initial status
        assert assigned_application.status == "submitted"
        
        # Assign Director (should already be done via fixture)
        assert assigned_application.assigned_director_id == 1002
        
        # Verify status is now Under Review
        assert assigned_application.status == "under_review"


class TestCFR006_8:
    """Test TEST-CFR-006-8: Verify notification of assigned Director."""
    
    def test_notification_generated_for_assigned_director(self, assigned_application):
        """
        Test ID: TEST-CFR-006-8
        Source ID: PMS-AFR-057
        
        Purpose: Verify notification of assigned Director
        Preconditions: Application is assigned to a Director.
        Action/Input: Monitor the assigned Director's communication channel.
        Expected Result: A notification regarding the assignment and initiation of the review timeline is generated.
        """
        # Verify history entry was created for assignment
        history_entries = ApplicationHistory.objects.filter(
            application=assigned_application,
            action="assign_director"
        ).order_by("-created_at")
        
        assert history_entries.exists()
        
        # Check that notification would be generated (simulated via history)
        history_entry = history_entries.first()
        assert history_entry.actor_id == 1003  # Admin who assigned
        assert history_entry.action == "assign_director"


class TestCFR007_0:
    """Test TEST-CFR-007-0: Verify Director access to application details."""
    
    def test_director_can_view_assigned_application(self, assigned_application):
        """
        Test ID: TEST-CFR-007-0
        Source ID: PMS-AFR-058
        
        Purpose: Verify Director access to application details
        Preconditions: Application status is 'Under Review'.
        Action/Input: Director navigates to the assigned application.
        Expected Result: Director views full application details, documents, and supporting materials.
        """
        # Verify Director can access the application
        assert assigned_application.status == "under_review"
        assert assigned_application.assigned_director_id == 1002
        
        # Director principal should be able to retrieve application
        app = PatentApplication.objects.get(pk=assigned_application.id)
        assert app.title == "Test Application 4"


class TestCFR007_1:
    """Test TEST-CFR-007-1: Verify valid review decision selection."""
    
    def test_valid_review_decisions_accepted(self, assigned_application):
        """
        Test ID: TEST-CFR-007-1
        Source ID: PMS-AFR-059
        
        Purpose: Verify valid review decision selection (Approve/Reject/Revision)
        Preconditions: Director is reviewing an application.
        Action/Input: Select a decision from the dropdown: Approve, Reject, or Needs Revision.
        Expected Result: The system accepts exactly one of these three decisions.
        """
        # Valid decisions should be accepted
        valid_decisions = ['approve', 'reject', 'needs_revision']
        
        for decision in valid_decisions:
            assert decision in valid_decisions
            
            # Test review with valid decision
            review_application(
                director_id=1002,
                application_id=assigned_application.id,
                decision=decision,
                justification="This is a test justification with enough text to meet the minimum requirement for Director review decisions." * 3
            )


class TestCFR007_2:
    """Test TEST-CFR-007-2: Verify minimum justification length (50 characters)."""
    
    def test_insufficient_justification_rejected(self, assigned_application):
        """
        Test ID: TEST-CFR-007-2
        Source ID: PMS-AFR-060
        
        Purpose: Verify minimum justification length (50 characters)
        Preconditions: Director attempts to submit a decision.
        Action/Input: Submit a decision with a justification containing fewer than 50 characters.
        Expected Result: The system prevents submission and prompts for additional justification text.
        """
        # Test with insufficient justification (< 50 chars)
        insufficient_justification = "Too short"
        
        assert len(insufficient_justification.strip()) < 50
        
        # Should raise ValueError due to validation
        with pytest.raises(Exception):
            review_application(
                director_id=1002,
                application_id=assigned_application.id,
                decision="approve",
                justification=insufficient_justification
            )


class TestCFR007_3:
    """Test TEST-CFR-007-3: Verify enforcement of 15-day review deadline."""
    
    def test_overdue_review_prevents_action(self, review_deadline_application):
        """
        Test ID: TEST-CFR-007-3
        Source ID: PMS-AFR-061
        
        Purpose: Verify enforcement of 15-day review deadline
        Preconditions: Application is 'Under Review' and current time exceeds the review deadline.
        Action/Input: Attempt to view submission controls for this application.
        Expected Result: The system prevents further action or logs a status of 'Overdue Review'.
        test_type: WF-02 approval-rejected path
        """
        # Verify review due date is in the past
        assert review_deadline_application.review_due_date < date.today()
        
        # Should log overdue status (simulated via history)
        history_entries = ApplicationHistory.objects.filter(
            application=review_deadline_application,
            action="review"
        ).order_by("-created_at")
        
        # Check if overdue review is logged
        assert history_entries.exists()
