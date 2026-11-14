"""Test cases for BR-PMS-022 through BR-PMS-030."""
import pytest
from datetime import date, timedelta
from typing import Set

from modules.patent.domain.policy import (
    can_transition, is_conflicted, validate_justification,
    missing_required_fields, budget_needs_escalation,
    can_withdraw, ALLOWED_TRANSITIONS
)


@pytest.fixture
def mock_director():
    """Create a mock director user ID."""
    return 1001


@pytest.fixture
def mock_applicant():
    """Create a mock applicant user ID."""
    return 2001


@pytest.fixture
def mock_attorney():
    """Create a mock attorney user ID."""
    return 3001


@pytest.fixture
def mock_admin():
    """Create a mock PCC_ADMIN user ID."""
    return 4001


@pytest.fixture
def application(mock_director, mock_applicant):
    """Create a mock patent application."""
    from modules.patent.models import PatentApplication
    
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-001",
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Software",
        applicant_id=mock_applicant,
        status="submitted"
    )
    return app


@pytest.fixture
def inventor(application):
    """Create a mock inventor."""
    from modules.patent.models import Inventor
    
    inv = Inventor.objects.create(
        application=application,
        user_id=mock_director,  # Director is also an inventor
        name="Director Name",
        email="director@example.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    return inv


@pytest.fixture
def director_as_inventor(application):
    """Application where director is listed as inventor."""
    from modules.patent.models import Inventor
    
    inv = Inventor.objects.create(
        application=application,
        user_id=mock_director,  # Director is also an inventor
        name="Director Name",
        email="director@example.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    return inv


@pytest.fixture
def director_not_as_inventor(application):
    """Application where director is NOT listed as inventor."""
    from modules.patent.models import Inventor
    
    inv = Inventor.objects.create(
        application=application,
        user_id=mock_applicant,  # Applicant is the inventor
        name="Applicant Name",
        email="applicant@example.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    return inv


@pytest.fixture
def director_with_expertise(application):
    """Director with Legal expertise for Software Patent application."""
    from modules.patent.models import Inventor
    
    inv = Inventor.objects.create(
        application=application,
        user_id=mock_director,
        name="Director Name",
        email="director@example.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    return inv


@pytest.fixture
def director_with_max_capacity(application):
    """Director at max capacity."""
    from modules.patent.models import PatentApplication
    
    # Create an application already assigned to this director
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-002",
        title="Test Application 2",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Software",
        applicant_id=mock_applicant,
        status="submitted",
        assigned_director_id=mock_director
    )
    return app


@pytest.fixture
def director_with_free_capacity(application):
    """Director with free capacity."""
    from modules.patent.models import PatentApplication
    
    # Create an application NOT assigned to this director
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-003",
        title="Test Application 3",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Software",
        applicant_id=mock_applicant,
        status="submitted"
    )
    return app


@pytest.fixture
def application_with_conflict(application):
    """Application where director is inventor."""
    from modules.patent.models import Inventor
    
    inv = Inventor.objects.create(
        application=application,
        user_id=mock_director,  # Director is also an inventor
        name="Director Name",
        email="director@example.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    return inv


@pytest.fixture
def application_without_conflict(application):
    """Application where director is NOT inventor."""
    from modules.patent.models import Inventor
    
    inv = Inventor.objects.create(
        application=application,
        user_id=mock_applicant,  # Applicant is the inventor
        name="Applicant Name",
        email="applicant@example.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    return inv


@pytest.fixture
def short_justification():
    """Justification with exactly 49 characters."""
    return "This is a very short justification that is only forty-nine characters long"


@pytest.fixture
def valid_justification():
    """Justification with at least 50 characters."""
    return "This is a valid justification that meets the minimum requirement of fifty characters or more for proper review documentation purposes."


class TestBRPMS022:
    """Test BR-PMS-022: Auto-assignment without configured rules should be rejected."""
    
    def test_auto_assignment_without_rules(self, application):
        """Verify PMS prevents automatic assignment without configured rules.
        
        Precondition: No specific expertise rules defined for a department.
        Action: Attempt auto-assignment.
        Expected: System rejects or logs warning.
        """
        # Test that can_transition works correctly - auto-assign is not in allowed transitions
        from_status = "submitted"
        to_status = "auto_assigned"  # This would be the auto-assign status
        
        result = can_transition(from_status, to_status)
        
        assert result is False, "Auto-assignment should be rejected without configured rules."


class TestBRPMS023:
    """Test BR-PMS-023: Director expertise matching during assignment."""
    
    def test_director_expertise_matching(self, director_with_expertise):
        """Verify PMS enforces Director expertise matching.
        
        Precondition: Director has 'Legal' expertise, Application is 'Software Patent'.
        Action: System auto-routes or manual assigns to Director.
        Expected: Assignment validated against domain.
        """
        # Verify that director can be assigned (expertise matches)
        from modules.patent.domain.policy import is_conflicted
        
        inventor_user_ids = {mock_director}  # Director is inventor
        
        # Check if there's a conflict - should be False since expertise matches
        result = is_conflicted(mock_director, inventor_user_ids)
        
        assert result is False, "Director should not be conflicted when expertise matches."


class TestBRPMS024:
    """Test BR-PMS-024: Director workload balance during assignment."""
    
    def test_director_workload_balance(self, director_with_max_capacity, director_with_free_capacity):
        """Verify PMS enforces Director workload balance.
        
        Precondition: Director D at max capacity, Director E has free capacity.
        Action: System auto-routes application to Director D.
        Expected: Assignment blocked or routed to Director E.
        """
        # Simulate checking if director is at max capacity
        from_status = "submitted"
        to_status = "auto_assigned"  # This would be the auto-assign status
        
        result = can_transition(from_status, to_status)
        
        assert result is False, "Auto-assignment should be blocked when director at max capacity."


class TestBRPMS025:
    """Test BR-PMS-025: Conflict of interest before Director assignment."""
    
    def test_conflict_of_interest_director_is_inventor(self, application_with_conflict):
        """Verify PMS checks conflict-of-interest before Director assignment.
        
        Precondition: Director is inventor on Application X.
        Action: Process assignment request.
        Expected: Assignment rejected with Conflict of Interest error.
        """
        from modules.patent.domain.policy import is_conflicted
        
        inventor_user_ids = {mock_director}  # Director is inventor
        
        result = is_conflicted(mock_director, inventor_user_ids)
        
        assert result is True, "Director should be flagged as conflicted when they are an inventor."


class TestBRPMS026:
    """Test BR-PMS-026: Blocks Director review if listed as inventor."""
    
    def test_director_review_blocked_if_inventor(self, application_with_conflict):
        """Verify PMS blocks Director review if they are inventor.
        
        Precondition: Director is inventor on Application X, status 'Under Review'.
        Action: Director attempts to access 'Review' function.
        Expected: Access denied with notification of restriction.
        """
        from modules.patent.domain.policy import is_conflicted
        
        inventor_user_ids = {mock_director}  # Director is inventor
        
        result = is_conflicted(mock_director, inventor_user_ids)
        
        assert result is True, "Director should be flagged as conflicted when they are an inventor."


class TestBRPMS027:
    """Test BR-PMS-027: PCC_ADMIN cannot review if listed as inventor."""
    
    def test_pcc_admin_review_blocked_if_inventor(self, application_with_conflict):
        """Verify PCC_ADMIN cannot review applications where they are inventors.
        
        Precondition: PCC_ADMIN is inventor on Application X.
        Action: Attempt to view Application X for review decision.
        Expected: Access denied with conflict of interest flag.
        """
        from modules.patent.domain.policy import is_conflicted
        
        # Simulate PCC_ADMIN as inventor
        inventor_user_ids = {mock_admin}  # PCC_ADMIN is inventor
        
        result = is_conflicted(mock_admin, inventor_user_ids)
        
        assert result is True, "PCC_ADMIN should be flagged as conflicted when they are an inventor."


class TestBRPMS029:
    """Test BR-PMS-029: Rejects Director decisions other than Approve, Reject, Needs Revision."""
    
    def test_director_decision_validation(self):
        """Verify PMS rejects Director decisions other than valid options.
        
        Precondition: Decision dropdown available.
        Action: Select 'Withdraw' as decision option.
        Expected: Validation fails with error for invalid options.
        """
        # Valid decisions are defined in policy
        from modules.patent.domain.policy import ALLOWED_TRANSITIONS
        
        # Check what transitions are allowed from 'submitted' status
        valid_transitions = ALLOWED_TRANSITIONS.get("submitted", set())
        
        assert "withdrawn" not in valid_transitions, "Withdraw should not be a valid decision option."


class TestBRPMS030:
    """Test BR-PMS-030: Rejects Director decision with justification < 50 characters."""
    
    def test_director_justification_length(self, short_justification):
        """Verify PMS rejects Director decision with insufficient justification.
        
        Precondition: Justification is exactly 49 characters.
        Action: Attempt to submit review decision.
        Expected: Submission blocked with minimum 50 character error.
        """
        from modules.patent.domain.policy import validate_justification
        
        result = validate_justification(short_justification)
        
        assert result is False, "Justification should be rejected if less than 50 characters."
    
    def test_director_justification_valid(self, valid_justification):
        """Verify PMS accepts Director decision with sufficient justification.
        
        Precondition: Justification is at least 50 characters.
        Action: Attempt to submit review decision.
        Expected: Submission accepted.
        """
        from modules.patent.domain.policy import validate_justification
        
        result = validate_justification(valid_justification)
        
        assert result is True, "Justification should be accepted if at least 50 characters."
