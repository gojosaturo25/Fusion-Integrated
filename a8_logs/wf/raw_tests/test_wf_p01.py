"""Automated backend tests for Patent Management System workflow cases T-001 to T-008."""
import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument, AttorneyAssignment,
    Budget, Appeal, ApplicationHistory
)
from modules.patent.services.applications import (
    submit_application, assign_director, review_application, resubmit_application,
    withdraw_application, expire_overdue_resubmissions, file_appeal, decide_appeal
)
from modules.patent.domain.policy import (
    can_transition, validate_justification, add_business_days, review_due_date,
    resubmission_deadline, is_conflicted, can_withdraw
)


# -----------------------------------------------------------------------------
# Test Fixtures and Setup Helpers
# -----------------------------------------------------------------------------

@pytest.fixture
def valid_applicant():
    """Create a valid applicant user reference."""
    return type('UserRef', (), {
        'user_id': 1001,
        'username': 'u1001',
        'display_name': 'Test Applicant',
        'kind': 'student',
        'discipline': 'CSE'
    })()


@pytest.fixture
def valid_director():
    """Create a valid director user reference."""
    return type('UserRef', (), {
        'user_id': 2001,
        'username': 'u2001',
        'display_name': 'Test Director',
        'kind': 'faculty',
        'discipline': 'CSE'
    })()


@pytest.fixture
def valid_attorney():
    """Create a valid attorney user reference."""
    return type('UserRef', (), {
        'user_id': 3001,
        'username': 'u3001',
        'display_name': 'Test Attorney',
        'kind': 'staff',
        'discipline': 'Legal'
    })()


@pytest.fixture
def application_data():
    """Return valid application data for testing."""
    return {
        'title': 'Innovative Patent Application',
        'abstract': 'A brief description of the invention.',
        'description': 'Detailed technical description of the patent invention.',
        'claims': 'The claimed invention includes...',
        'technical_domain': 'Computer Science'
    }


@pytest.fixture
def valid_documents():
    """Return valid document data for testing."""
    return [
        {
            'file_name': 'application_draft.pdf',
            'content_type': 'application/pdf',
            'size': 1024 * 100,  # 100KB under 50MB limit
        },
        {
            'file_name': 'technical_specification.pdf',
            'content_type': 'application/pdf',
            'size': 500 * 1024,  # 500KB under 50MB limit
        }
    ]


@pytest.fixture
def valid_inventors():
    """Return valid inventor data for testing."""
    return [
        {
            'user_id': 1001,
            'name': 'John Doe',
            'email': 'john@example.com',
            'contribution_percent': 50.0,
            'agreement_signed': True
        },
        {
            'user_id': 1002,
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'contribution_percent': 50.0,
            'agreement_signed': True
        }
    ]


# -----------------------------------------------------------------------------
# Test Case T-001: Application Submission Validation
# -----------------------------------------------------------------------------

class TestT001ApplicationSubmission(TestCase):
    """Test case T-001 from UC-PMS-001."""
    
    def test_001_valid_submission_validation_and_id_assignment(self):
        """
        Validate submission validation, document compliance, and application ID assignment 
        upon a valid initial submission.
        
        Test ID: T-001
        Source ID: UC-PMS-001
        Purpose: Validate submission validation, document compliance, and application ID assignment 
                 upon a valid initial submission.
        Preconditions: System running; Application draft exists with required fields, PDF documents 
                      under 50MB, and completed inventor agreement.
        Action/Input: Applicant submits the patent application via UC-PMS-001.
        Expected Result: PMS validates requirements, assigns unique Application ID, sets status 
                        to 'Submitted', records history, and notifies stakeholders.
        Test Type: Functional
        """
        # Arrange
        applicant_id = 1001
        data = application_data.copy()
        inventors = valid_inventors
        documents = valid_documents
        actor_id = applicant_id
        
        # Act
        app = submit_application(
            applicant_id=applicant_id,
            data=data,
            inventors=inventors,
            documents=documents,
            actor_id=actor_id
        )
        
        # Assert
        self.assertIsNotNone(app.id, "Application ID should be assigned")
        self.assertEqual(app.status, 'submitted', "Status should be set to 'Submitted'")
        self.assertEqual(len(inventors), app.inventors.count(), "All inventors should be created")
        self.assertEqual(len(documents), app.documents.count(), "All documents should be created")
        
        # Verify history record was created
        history = ApplicationHistory.objects.filter(application=app).first()
        self.assertIsNotNone(history, "Application history should be recorded")
        self.assertEqual(history.action, 'submit', "History action should be 'submit'")


# -----------------------------------------------------------------------------
# Test Case T-002: Assignment Logic with Conflict Checks
# -----------------------------------------------------------------------------

class TestT002AssignmentLogic(TestCase):
    """Test case T-002 from UC-PMS-007."""
    
    def test_002_assignment_logic_with_conflict_check(self):
        """
        Validate assignment logic including expertise matching, conflict-of-interest checks, 
        and status transition to 'Under Review'.
        
        Test ID: T-002
        Source ID: UC-PMS-007
        Purpose: Validate assignment logic including expertise matching, conflict-of-interest 
                checks, and status transition to 'Under Review'.
        Preconditions: Application is in 'Submitted' state; Eligible Directors exist.
        Action/Input: PCC_ADMIN assigns the application to a Director (explicit or automatic routing).
        Expected Result: PMS verifies assignment criteria, rejects invalid conflicts if applicable, 
                        and updates status to 'Under Review' with notifications.
        Test Type: Functional
        """
        # Arrange
        applicant_id = 1001
        director_id = 2001
        
        # Create application in submitted state
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-001',
            title='Test Application',
            abstract='Test Abstract',
            description='Test Description',
            claims='Test Claims',
            technical_domain='CSE',
            applicant_id=applicant_id,
            status='submitted'
        )
        
        # Create inventor that matches director (conflict scenario)
        Inventor.objects.create(
            application=app,
            user_id=director_id,  # Director is also an inventor - conflict!
            name='Director as Inventor',
            email='director@example.com',
            contribution_percent=50.0,
            agreement_signed=True
        )
        
        # Act - Try to assign director who is conflicted (should fail)
        with self.assertRaises(ValueError):
            assign_director(
                admin_id=1,  # PCC_ADMIN
                application_id=app.id,
                director_id=director_id
            )
        
        # Assert - Verify conflict was detected
        inventors = Inventor.objects.filter(application=app)
        inventor_user_ids = inventors.values_list('user_id', flat=True)
        self.assertTrue(is_conflicted(director_id, inventor_user_ids), 
                       "Director should be conflicted with inventor")


# -----------------------------------------------------------------------------
# Test Case T-003: Director Review with Justification Validation
# -----------------------------------------------------------------------------

class TestT003DirectorReview(TestCase):
    """Test case T-003 from BR-PMS-029; BR-PMS-030; BR-PMS-031."""
    
    def test_003_director_review_with_justification_validation(self):
        """
        Validate Director's review process, justification length enforcement, status transition on approval.
        
        Test ID: T-003
        Source ID: BR-PMS-029; BR-PMS-030; BR-PMS-031
        Purpose: Validate Director's review process, justification length enforcement, status 
                transition on approval.
        Preconditions: Application is in 'Under Review' state with valid documentation.
        Action/Input: Director reviews the application and provides a detailed justification 
                     of at least 50 characters; decides to Approve.
        Expected Result: PMS stores decision, validates justification length, updates status 
                        to 'Approved', and notifies relevant parties.
        Test Type: Functional
        """
        # Arrange
        applicant_id = 1001
        director_id = 2001
        
        # Create application in under_review state
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-002',
            title='Test Application',
            abstract='Test Abstract',
            description='Test Description',
            claims='Test Claims',
            technical_domain='CSE',
            applicant_id=applicant_id,
            status='under_review'
        )
        
        # Assign director
        assign_director(
            admin_id=1,
            application_id=app.id,
            director_id=director_id
        )
        
        # Act - Director reviews with valid justification (>= 50 chars)
        long_justification = 'This is a detailed justification that meets the minimum requirement of fifty characters or more for proper review documentation.'
        
        app = review_application(
            director_id=director_id,
            application_id=app.id,
            decision='approve',
            justification=long_justification
        )
        
        # Assert
        self.assertEqual(app.status, 'approved', "Status should be updated to 'Approved'")
        self.assertIsNotNone(app.latest_decision, "Latest decision should be stored")
        self.assertEqual(app.latest_decision, 'approve', "Decision should match input")
        self.assertGreater(len(app.latest_justification), 50, "Justification should be at least 50 characters")


# -----------------------------------------------------------------------------
# Test Case T-004: Revision Submission Loop
# -----------------------------------------------------------------------------

class TestT004RevisionSubmission(TestCase):
    """Test case T-004 from BR-PMS-029; BR-PMS-030; BR-PMS-031; BR-PMS-033."""
    
    def test_004_revision_submission_within_deadline(self):
        """
        Validate revision submission loop where applicant addresses feedback within the 60-day 
        resubmission period.
        
        Test ID: T-004
        Source ID: BR-PMS-029; BR-PMS-030; BR-PMS-031; BR-PMS-033
        Purpose: Validate revision submission loop where applicant addresses feedback within the 
                60-day resubmission period.
        Preconditions: Application status is 'Needs Revision' or 'Rejected' with valid Director 
                      justification logged.
        Action/Input: Applicant resubmits application addressing Director's feedback within 
                     the applicable 60-day window via UC-PMS-005.
        Expected Result: PMS validates deadline compliance and content alignment, assigns new 
                        Application ID/Version control cycle, updates status to 'Submitted' or 
                        re-routes to assignment.
        Test Type: Functional
        """
        # Arrange
        applicant_id = 1001
        
        # Create application in needs_revision state with resubmission deadline set
        decision_date = date.today() - timedelta(days=30)
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-003',
            title='Test Application',
            abstract='Test Abstract',
            description='Test Description',
            claims='Test Claims',
            technical_domain='CSE',
            applicant_id=applicant_id,
            status='needs_revision',
            resubmission_deadline=resubmission_deadline(decision_date)  # Should be within 60 days
        )
        
        # Act - Applicant resubmits within deadline
        changes = {
            'title': 'Updated Title',
            'description': 'Updated Description'
        }
        response_to_feedback = 'We have addressed all concerns raised by the Director.'
        
        app = resubmit_application(
            applicant_id=applicant_id,
            application_id=app.id,
            changes=changes,
            response_to_feedback=response_to_feedback,
            actor_id=applicant_id
        )
        
        # Assert
        self.assertEqual(app.status, 'resubmitted', "Status should be updated to 'Resubmitted'")
        self.assertGreater(app.version_number, 1, "Version number should be incremented")
        self.assertIsNotNone(app.resubmission_deadline, "New resubmission deadline should be set")


# -----------------------------------------------------------------------------
# Test Case T-005: Automatic Expiration on Deadline Miss
# -----------------------------------------------------------------------------

class TestT005AutomaticExpiration(TestCase):
    """Test case T-005 from BR-PMS-038."""
    
    def test_005_automatic_status_transition_to_expired(self):
        """
        Validate automatic status transition to 'Expired' when resubmission deadline expires 
        (system-enforced behavior).
        
        Test ID: T-005
        Source ID: BR-PMS-038
        Purpose: Validate automatic status transition to 'Expired' when resubmission deadline 
                expires (system-enforced behavior).
        Preconditions: Application is in 'Needs Revision' state; Applicant has failed to 
                      resubmit within the applicable 60-day period.
        Action/Input: System checks the current date against the rejection/revision decision 
                     date and applies rule BR-PMS-038.
        Expected Result: PMS automatically updates the application status to 'Expired' without 
                        actor intervention.
        Test Type: System
        """
        # Arrange
        applicant_id = 1001
        
        # Create application in needs_revision state with past resubmission deadline
        decision_date = date.today() - timedelta(days=90)  # Past decision date
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-004',
            title='Test Application',
            abstract='Test Abstract',
            description='Test Description',
            claims='Test Claims',
            technical_domain='CSE',
            applicant_id=applicant_id,
            status='needs_revision',
            resubmission_deadline=date.today() - timedelta(days=30)  # Past deadline
        )
        
        # Act - System checks and expires application
        today = date.today()
        expired_apps = expire_overdue_resubmissions(today)
        
        # Assert
        self.assertIn(app, expired_apps, "Application should be in expired list")
        self.assertEqual(app.status, 'expired', "Status should be updated to 'Expired'")
        
        # Verify history record was created
        history = ApplicationHistory.objects.filter(application=app).filter(action='expire').first()
        self.assertIsNotNone(history, "Expiration history should be recorded")


# -----------------------------------------------------------------------------
# Test Case T-006: Appeal Submission Rules
# -----------------------------------------------------------------------------

class TestT006AppealSubmission(TestCase):
    """Test case T-006 from UC-PMS-022."""
    
    def test_006_appeal_submission_rules_and_status_transition(self):
        """
        Validate appeal submission rules, grounds justification recording, and transition to 
        'Appeal Submitted'.
        
        Test ID: T-006
        Source ID: UC-PMS-022
        Purpose: Validate appeal submission rules, grounds justification recording, and transition 
                to 'Appeal Submitted'.
        Preconditions: Application status is 'Rejected' with valid Director justification.
        Action/Input: Applicant initiates the File Appeal Against Rejection process (UC-PMS-022) 
                     within the allowed time period.
        Expected Result: PMS validates appeal deadline, records grounds/justification, updates 
                        status to 'Appeal Submitted', and notifies Director.
        Test Type: Functional
        """
        # Arrange
        applicant_id = 1001
        
        # Create application in rejected state
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-005',
            title='Test Application',
            abstract='Test Abstract',
            description='Test Description',
            claims='Test Claims',
            technical_domain='CSE',
            applicant_id=applicant_id,
            status='rejected'
        )
        
        # Act - Applicant files appeal
        grounds = 'The rejection was based on incorrect interpretation of the claims.'
        
        appeal = file_appeal(
            applicant_id=applicant_id,
            application_id=app.id,
            grounds=grounds
        )
        
        # Assert
        self.assertIsNotNone(appeal.id, "Appeal ID should be assigned")
        self.assertEqual(appeal.status, 'submitted', "Status should be 'Appeal Submitted'")
        self.assertEqual(appeal.grounds, grounds, "Grounds should match input")


# -----------------------------------------------------------------------------
# Test Case T-007: Director Modifies Decision During Appeal
# -----------------------------------------------------------------------------

class TestT007DirectorModifyDecision(TestCase):
    """Test case T-007 from BR-PMS-095."""
    
    def test_007_director_modifies_decision_during_appeal(self):
        """
        Validate Director's ability to modify a rejected application decision during an appeal 
        review.
        
        Test ID: T-007
        Source ID: BR-PMS-095
        Purpose: Validate Director's ability to modify a rejected application decision during 
                an appeal review.
        Preconditions: Application is in 'Appeal Submitted' state after being Rejected.
        Action/Input: Director reviews the appeal and decides to 'Modify Decision'.
        Expected Result: PMS records the modification outcome, initiates next applicable process 
                        step (e.g., resubmission or new review cycle), and updates status accordingly.
        Test Type: Functional
        """
        # Arrange
        applicant_id = 1001
        director_id = 2001
        
        # Create application in rejected state
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-006',
            title='Test Application',
            abstract='Test Abstract',
            description='Test Description',
            claims='Test Claims',
            technical_domain='CSE',
            applicant_id=applicant_id,
            status='rejected'
        )
        
        # Create appeal
        grounds = 'The rejection was based on incorrect interpretation of the claims.'
        appeal = file_appeal(
            applicant_id=applicant_id,
            application_id=app.id,
            grounds=grounds
        )
        
        # Update application status to appeal_submitted
        app.status = 'appeal_submitted'
        app.save()
        
        # Act - Director modifies decision
        outcome = 'modify_decision'
        justification = 'The original rejection was based on a misunderstanding of the patent claims.'
        
        appeal = decide_appeal(
            director_id=director_id,
            appeal_id=appeal.id,
            outcome=outcome,
            justification=justification
        )
        
        # Assert
        self.assertEqual(appeal.status, 'decision_modified', "Status should be updated to 'Decision Modified'")
        self.assertIsNotNone(appeal.decided_by, "Director ID should be recorded")
        self.assertEqual(appeal.justification, justification, "Justification should match input")


# -----------------------------------------------------------------------------
# Test Case T-008: Escalation Handling for Budget Cases
# -----------------------------------------------------------------------------

class TestT008EscalationHandling(TestCase):
    """Test case T-008 from UC-PMS-027."""
    
    def test_008_escalation_handling_for_budget_cases(self):
        """
        Validate escalation handling and PCC_ADMIN monitoring for budget cases exceeding 
        threshold limits.
        
        Test ID: T-008
        Source ID: UC-PMS-027
        Purpose: Validate escalation handling and PCC_ADMIN monitoring for budget cases 
                exceeding threshold limits.
        Preconditions: Application is 'Approved'; Budget review decision outcome is 'Escalated' 
                      (cost > threshold).
        Action/Input: Director routes/escalates the case (simulating BR-PMS-051 outcome).
        Expected Result: PCC_ADMIN monitors and tracks the exceptional case, maintains status 
                        as 'Escalation Tracked / External Decision Pending' within PMS scope.
        Test Type: Functional
        """
        # Arrange
        applicant_id = 1001
        director_id = 2001
        
        # Create application in approved state
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-007',
            title='Test Application',
            abstract='Test Abstract',
            description='Test Description',
            claims='Test Claims',
            technical_domain='CSE',
            applicant_id=applicant_id,
            status='approved'
        )
        
        # Create budget with high cost (exceeds threshold)
        from decimal import Decimal
        budget = Budget.objects.create(
            application=app,
            filing_fee=Decimal('5000.00'),
            attorney_fee=Decimal('3000.00'),
            administrative_cost=Decimal('2000.00'),
            total=Decimal('10000.00'),  # Exceeds typical threshold of 5000
            status='pending',
            decided_by=None,
            justification=''
        )
        
        # Act - Director escalates budget (simulating BR-PMS-051 outcome)
        from decimal import Decimal
        escalated = False
        
        updated_budget, escalated = decide_budget(
            director_id=director_id,
            budget_id=budget.id,
            approve=False,  # Reject due to exceeding threshold
            justification='Budget exceeds the approved threshold of $5000.00.',
            threshold=Decimal('5000.00')
        )
        
        # Assert
        self.assertTrue(escalated, "Budget should be escalated")
        self.assertEqual(updated_budget.status, 'escalated', "Status should be 'Escalated'")
        self.assertIsNotNone(updated_budget.decided_by, "Director ID should be recorded")
        self.assertGreater(updated_budget.total, Decimal('5000.00'), "Total should exceed threshold")


# -----------------------------------------------------------------------------
# Additional Helper Functions for Testing
# -----------------------------------------------------------------------------

def get_application_number(app):
    """Helper to get application number from model."""
    return app.APPLICATION_NUMBER if hasattr(app, 'APPLICATION_NUMBER') else str(app.id)


def verify_history_record(app, action, actor_id=None):
    """Helper to verify history record was created for an application."""
    history = ApplicationHistory.objects.filter(application=app).filter(action=action).first()
    return history is not None and (actor_id is None or history.actor_id == actor_id)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
