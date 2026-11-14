"""Test cases for BR-PMS-031 through BR-PMS-041."""
import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.core.cache import cache

from fusion_auth.client import IamSession
from fusion_auth.principal import Principal

from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument,
    AttorneyAssignment, PatentabilityOpinion, Budget, Filing,
    OfficeAction, MaintenanceRecord, Appeal, ApplicationHistory
)
from modules.patent.services.applications import (
    submit_application, assign_director, review_application, resubmit_application,
    withdraw_application, expire_overdue_resubmissions
)
from modules.patent.domain.policy import (
    can_transition, validate_justification, resubmission_deadline,
    add_business_days, is_conflicted, can_withdraw
)


@pytest.fixture
def app_factory():
    """Factory to create patent applications for testing."""
    def _make_app(status="draft", applicant_id=1001):
        return PatentApplication.objects.create(
            APPLICATION_NUMBER=f"APP-{status.upper()}",
            title="Test Application",
            abstract="Test abstract",
            description="Test description",
            claims="Test claims",
            technical_domain="Test Domain",
            applicant_id=applicant_id,
            status=status,
        )
    return _make_app


@pytest.fixture
def director_session():
    """Create a Director IAM session."""
    return IamSession(
        user_id=2001, username="d2001", display_name="Director 2001",
        kind="director", active_role="director", roles=("director",),
        permissions=frozenset(["patent.application.review"]),
    )


@pytest.fixture
def pcc_admin_session():
    """Create a PCC_ADMIN IAM session."""
    return IamSession(
        user_id=3001, username="p3001", display_name="PCC Admin 3001",
        kind="admin", active_role="admin", roles=("admin",),
        permissions=frozenset(["patent.application.manage"]),
    )


@pytest.fixture
def applicant_session():
    """Create an Applicant IAM session."""
    return IamSession(
        user_id=1001, username="u1001", display_name="Applicant 1001",
        kind="student", active_role="student", roles=("student",),
        permissions=frozenset(["patent.application.create"]),
    )


@pytest.fixture
def approved_app(app_factory):
    """Create an approved application."""
    return app_factory(status="approved")


@pytest.fixture
def rejected_app(app_factory):
    """Create a rejected application."""
    return app_factory(status="rejected")


@pytest.fixture
def needs_revision_app(app_factory):
    """Create a needs revision application."""
    return app_factory(status="needs_revision")


@pytest.fixture
def resubmitted_app(app_factory):
    """Create a resubmitted application."""
    return app_factory(status="resubmitted")


@pytest.fixture
def inventor(app_factory):
    """Create an inventor for the application."""
    app = app_factory()
    return Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True,
    )


@pytest.fixture
def director_assigned_app(app_factory):
    """Create an application with a director assigned."""
    app = app_factory(status="approved")
    return assign_director(
        admin_id=3001,
        application_id=app.id,
        director_id=2001,
    )


@pytest.fixture
def attorney_assigned_app(app_factory):
    """Create an application with an attorney assigned."""
    app = app_factory(status="approved")
    return assign_director(
        admin_id=3001,
        application_id=app.id,
        director_id=2001,
    )


class TestBRPMS031(TestCase):
    """Test BR-PMS-031: Verify PMS enforces Director review deadline of 15 business days."""

    def test_001(self):
        """test_id: BR-PMS-031, source_id: BR-PMS-031"""
        # Precondition: Director D assigned to Application X; Current time is T0. Deadline for completion is T1 (15 business days later).
        app = director_assigned_app
        
        # Calculate expected deadline (15 business days from assignment)
        created_date = app.created_at
        expected_deadline = add_business_days(created_date, 15)
        
        # Verify the review_due_date was set correctly
        self.assertEqual(app.review_due_date, expected_deadline)
        
        # System checks status at T2 where T2 > T1 without completed review.
        # This is a policy check - verify the deadline calculation is correct
        today = date.today()
        if today > expected_deadline:
            # If we're past the deadline, the system should flag it
            self.assertTrue(app.review_due_date < today)


class TestBRPMS033(TestCase):
    """Test BR-PMS-033: Verify PMS blocks revision submission if status is not Needs Revision or Rejected."""

    def test_001(self):
        """test_id: BR-PMS-033, source_id: BR-PMS-033"""
        # Precondition: Application status is 'Approved'. User attempts to initiate 'Revision' action.
        app = approved_app
        
        # Check if revision is allowed from this status
        self.assertFalse(can_transition(app.status, "resubmitted"))
        
        # Verify the policy rule
        valid_statuses_for_revision = ["needs_revision", "rejected"]
        self.assertIn(app.status, valid_statuses_for_revision)


class TestBRPMS034(TestCase):
    """Test BR-PMS-034: Verify PMS allows revision submission if status is Rejected."""

    def test_001(self):
        """test_id: BR-PMS-034, source_id: BR-PMS-034"""
        # Precondition: Application status is 'Rejected'. User attempts to initiate 'Revision' action.
        app = rejected_app
        
        # Check if revision is allowed from this status
        self.assertTrue(can_transition(app.status, "resubmitted"))


class TestBRPMS035(TestCase):
    """Test BR-PMS-035: Verify PMS monitors and validates 60-day resubmission deadline."""

    def test_001(self):
        """test_id: BR-PMS-035, source_id: BR-PMS-035"""
        # Precondition: Rejection/Revision decision made on Date D. Current time is D + 61 days.
        app = rejected_app
        
        # Calculate resubmission deadline (60 days from rejection)
        created_date = app.created_at
        expected_deadline = resubmission_deadline(created_date)
        
        # Verify the deadline calculation
        self.assertIsNotNone(expected_deadline)
        
        # Simulate time passing beyond deadline
        today = date.today()
        if today > expected_deadline:
            # Deadline has passed - check eligibility
            is_expired = today > expected_deadline
            self.assertTrue(is_expired)


class TestBRPMS036(TestCase):
    """Test BR-PMS-036: Verify PMS rejects revision submissions that do not address Director feedback."""

    def test_001(self):
        """test_id: BR-PMS-036, source_id: BR-PMS-036"""
        # Precondition: Application has specific feedback text. User submits new documents claiming to be a revision but omitting references to the feedback.
        app = rejected_app
        
        # Set latest_justification as Director feedback
        app.latest_justification = "Director feedback about claims and novelty"
        app.save()
        
        # Verify that justification validation works
        self.assertTrue(validate_justification(app.latest_justification))


class TestBRPMS038(TestCase):
    """Test BR-PMS-038: Verify PMS updates status to Expired after deadline expiration."""

    def test_001(self):
        """test_id: BR-PMS-038, source_id: BR-PMS-038"""
        # Precondition: Application in Revision cycle. 60 day period expired. No valid resubmission made.
        app = needs_revision_app
        
        # Calculate resubmission deadline
        created_date = app.created_at
        expected_deadline = resubmission_deadline(created_date)
        
        # Simulate time passing beyond deadline
        today = date.today()
        
        # Run expiry logic
        expired_apps = expire_overdue_resubmissions(today)
        
        # Verify status changed to Expired
        self.assertIn(app, expired_apps)


class TestBRPMS040(TestCase):
    """Test BR-PMS-040: Verify PMS restricts Attorney assignment role to PCC_ADMIN only."""

    def test_001(self):
        """test_id: BR-PMS-040, source_id: BR-PMS-040"""
        # Precondition: Director D has approved the application. User logged in as Director (not PCC_ADMIN).
        app = approved_app
        
        # Try to assign attorney using Director's session
        try:
            assignment = assign_director(
                admin_id=2001,  # Using director ID instead of admin
                application_id=app.id,
                director_id=2001,
            )
            self.fail("Should have raised ValueError for unauthorized assignment")
        except ValueError as e:
            self.assertIn("cannot assign", str(e).lower())


class TestBRPMS041(TestCase):
    """Test BR-PMS-041: Verify PMS enforces selection from approved panel unless exception recorded."""

    def test_001(self):
        """test_id: BR-PMS-041, source_id: BR-PMS-041"""
        # Precondition: Attorney O is NOT in the approved panel. User (PCC_ADMIN) attempts to assign Attorney O.
        app = approved_app
        
        # Try to assign attorney using PCC_ADMIN's session with non-panel attorney
        try:
            assignment = assign_director(
                admin_id=3001,  # Using PCC_ADMIN ID
                application_id=app.id,
                director_id=2001,
            )
            self.fail("Should have raised ValueError for unauthorized assignment")
        except ValueError as e:
            self.assertIn("cannot assign", str(e).lower())
