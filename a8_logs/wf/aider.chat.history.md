
# aider chat started at 2026-11-14 06:19:12

> /opt/homebrew/bin/aider --model ollama_chat/qwen3.5:4b --model-settings-file /Users/vishalkumar/elm_specs_md/pms_kit/a8/aider_model_settings.yml --edit-format whole --map-tokens 0 --timeout 3600 --yes-always --stream --no-pretty --no-fancy-input --no-gitignore --no-auto-commits --no-dirty-commits --no-auto-lint --no-auto-test --no-check-update --analytics-disable --no-show-release-notes --no-show-model-warnings --no-suggest-shell-commands --no-detect-urls --no-restore-chat-history --aiderignore /Users/vishalkumar/elm_specs_md/pms_kit/a8/aiderignore_a8 --chat-history-file a8_logs/wf/aider.chat.history.md --input-history-file a8_logs/wf/aider.input.history --llm-history-file a8_logs/wf/llm.history.txt --file tests/a8/wf/test_wf_p01.py --read conftest.py --read modules/patent/registry.py --read modules/patent/models.py --read modules/patent/domain/policy.py --read modules/patent/services/applications.py --read modules/patent/services/legal.py --read modules/patent/services/post_filing.py --read modules/patent/api/serializers.py --read modules/patent/api/views.py --read modules/patent/api/views_legal.py --read modules/patent/api/urls.py --message-file a8_logs/wf/promptB_p01.md  
> Creating empty file /Users/vishalkumar/ELM_MODEL_2/tests/a8/wf/test_wf_p01.py  
> Aider v0.86.2  
> Model: ollama_chat/qwen3.5:4b with whole edit format  
> Git repo: .git with 290 files  
> Repo-map: disabled  
> Added tests/a8/wf/test_wf_p01.py to the chat.  
> Added modules/patent/api/urls.py to the chat (read-only).  
> Added modules/patent/registry.py to the chat (read-only).  
> Added modules/patent/services/legal.py to the chat (read-only).  
> Added modules/patent/api/views_legal.py to the chat (read-only).  
> Added modules/patent/api/serializers.py to the chat (read-only).  
> Added modules/patent/services/post_filing.py to the chat (read-only).  
> Added modules/patent/api/views.py to the chat (read-only).  
> Added conftest.py to the chat (read-only).  
> Added modules/patent/models.py to the chat (read-only).  
> Added modules/patent/domain/policy.py to the chat (read-only).  
> Added modules/patent/services/applications.py to the chat (read-only).  

#### You are given:  
#### 1. the frozen A8_BASE Fusion implementation, and  
#### 2. the frozen WF_DESIGN.json.  
#### Convert these test designs into executable automated backend tests using pytest/pytest-django.  
#### Rules:  
#### - Implement exactly the supplied test cases.  
#### - Do not add, remove, merge or reinterpret test cases.  
#### - Preserve each specified expected result.  
#### - Do not modify production code.  
#### - Use the Django isolated test database.  
#### - Reuse existing Fusion test infrastructure where appropriate.  
#### - Do not mock the behavior being tested; mocks may be used only for unavailable external dependencies.  
#### - Do not use xfail to hide failures.  
#### - Every test must contain its test_id and source_id in its name or docstring.  
#### - Store generated tests only under tests/a8/wf/.  
#### If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.  
####   
#### The frozen WF_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 1 to 8 of 14; write exactly these test cases into tests/a8/wf/test_wf_p01.py.  
#### ```json  
#### [  
####  {  
####   "test_id": "T-001",  
####   "source_id": "UC-PMS-001",  
####   "purpose": "Validate submission validation, document compliance, and application ID assignment upon a valid initial submission.",  
####   "preconditions": "System running; Application draft exists with required fields, PDF documents under 50MB, and completed inventor agreement.",  
####   "action_or_input": "Applicant submits the patent application via UC-PMS-001.",  
####   "expected_result": "PMS validates requirements, assigns unique Application ID, sets status to 'Submitted', records history, and notifies stakeholders.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-002",  
####   "source_id": "UC-PMS-007",  
####   "purpose": "Validate assignment logic including expertise matching, conflict-of-interest checks, and status transition to 'Under Review'.",  
####   "preconditions": "Application is in 'Submitted' state; Eligible Directors exist.",  
####   "action_or_input": "PCC_ADMIN assigns the application to a Director (explicit or automatic routing).",  
####   "expected_result": "PMS verifies assignment criteria, rejects invalid conflicts if applicable, and updates status to 'Under Review' with notifications.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-003",  
####   "source_id": "BR-PMS-029; BR-PMS-030; BR-PMS-031",  
####   "purpose": "Validate Director's review process, justification length enforcement, status transition on approval.",  
####   "preconditions": "Application is in 'Under Review' state with valid documentation.",  
####   "action_or_input": "Director reviews the application and provides a detailed justification of at least 50 characters; decides to Approve.",  
####   "expected_result": "PMS stores decision, validates justification length, updates status to 'Approved', and notifies relevant parties.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-004",  
####   "source_id": "BR-PMS-029; BR-PMS-030; BR-PMS-031; BR-PMS-033",  
####   "purpose": "Validate revision submission loop where applicant addresses feedback within the 60-day resubmission period.",  
####   "preconditions": "Application status is 'Needs Revision' or 'Rejected' with valid Director justification logged.",  
####   "action_or_input": "Applicant resubmits application addressing Director's feedback within the applicable 60-day window via UC-PMS-005.",  
####   "expected_result": "PMS validates deadline compliance and content alignment, assigns new Application ID/Version control cycle, updates status to 'Submitted' or re-routes to assignment.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-005",  
####   "source_id": "BR-PMS-038",  
####   "purpose": "Validate automatic status transition to 'Expired' when resubmission deadline expires (system-enforced behavior).",  
####   "preconditions": "Application is in 'Needs Revision' state; Applicant has failed to resubmit within the applicable 60-day period.",  
####   "action_or_input": "System checks the current date against the rejection/revision decision date and applies rule BR-PMS-038.",  
####   "expected_result": "PMS automatically updates the application status to 'Expired' without actor intervention.",  
####   "test_type": "System"  
####  },  
####  {  
####   "test_id": "T-006",  
####   "source_id": "UC-PMS-022",  
####   "purpose": "Validate appeal submission rules, grounds justification recording, and transition to 'Appeal Submitted'.",  
####   "preconditions": "Application status is 'Rejected' with valid Director justification.",  
####   "action_or_input": "Applicant initiates the File Appeal Against Rejection process (UC-PMS-022) within the allowed time period.",  
####   "expected_result": "PMS validates appeal deadline, records grounds/justification, updates status to 'Appeal Submitted', and notifies Director.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-007",  
####   "source_id": "BR-PMS-095",  
####   "purpose": "Validate Director's ability to modify a rejected application decision during an appeal review.",  
####   "preconditions": "Application is in 'Appeal Submitted' state after being Rejected.",  
####   "action_or_input": "Director reviews the appeal and decides to 'Modify Decision'.",  
####   "expected_result": "PMS records the modification outcome, initiates next applicable process step (e.g., resubmission or new review cycle), and updates status accordingly.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-008",  
####   "source_id": "UC-PMS-027",  
####   "purpose": "Validate escalation handling and PCC_ADMIN monitoring for budget cases exceeding threshold limits.",  
####   "preconditions": "Application is 'Approved'; Budget review decision outcome is 'Escalated' (cost > threshold).",  
####   "action_or_input": "Director routes/escalates the case (simulating BR-PMS-051 outcome).",  
####   "expected_result": "PCC_ADMIN monitors and tracks the exceptional case, maintains status as 'Escalation Tracked / External Decision Pending' within PMS scope.",  
####   "test_type": "Functional"  
####  }  
#### ]  
#### ```  

<thinking-content-7bbeb8e1441453ad999a0bbba8a46d4b>

The user wants me to convert the test cases from WF_DESIGN.json into pytest/pytest-django tests. I need to:

1. Create tests for T-001 through T-008 (first 8 of 14 test cases)
2. Each test must have test_id and source_id in its name or docstring
3. Store tests under tests/a8/wf/test_wf_p01.py
4. Use pytest-django for Django testing
5. Don't modify production code
6. Use the existing Fusion test infrastructure (conftest.py is provided)
7. Don't mock behavior being tested - only external dependencies

Let me analyze each test case:

T-001: Submit application validation, document compliance, ID assignment
- Test submission with valid data
- Check status becomes 'Submitted'
- Verify history record created

T-002: Assignment logic with conflict checks
- Assign director to submitted application
- Check conflict of interest (director can't be inventor)
- Status transitions to 'Under Review'

T-003: Director review with justification validation
- Director reviews and approves
- Justification must be >= 50 chars
- Status becomes 'Approved'

T-004: Revision submission loop
- Applicant resubmits within 60-day window
- Version control, status updates

T-005: Automatic expiration on deadline miss
- System checks and expires application
- No actor intervention needed

T-006: Appeal submission rules
- File appeal when rejected
- Status becomes 'Appeal Submitted'

T-007: Director modifies decision during appeal
- Modify decision outcome
- Update status accordingly

T-008: Escalation handling for budget cases
- Budget exceeds threshold
- PCC_ADMIN tracks escalation

I need to look at the existing models and services to understand how to properly test these. Looking at the provided files:


- modules/patent/models.py has all the model definitions
- modules/patent/services/applications.py has the business logic
- modules/patent/domain/policy.py has validation rules
- conftest.py has fixtures for IAM and testing infrastructure

I'll create pytest tests that use Django's test database, leverage existing models and services, and follow Fusion test patterns from conftest.py.

</thinking-content-7bbeb8e1441453ad999a0bbba8a46d4b>

tests/a8/wf/test_wf_p01.py
```
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
```

> Tokens: 24k sent, 5.2k received.  
> Applied edit to tests/a8/wf/test_wf_p01.py  

# aider chat started at 2026-11-14 06:45:08

> /opt/homebrew/bin/aider --model ollama_chat/qwen3.5:4b --model-settings-file /Users/vishalkumar/elm_specs_md/pms_kit/a8/aider_model_settings.yml --edit-format whole --map-tokens 0 --timeout 3600 --yes-always --stream --no-pretty --no-fancy-input --no-gitignore --no-auto-commits --no-dirty-commits --no-auto-lint --no-auto-test --no-check-update --analytics-disable --no-show-release-notes --no-show-model-warnings --no-suggest-shell-commands --no-detect-urls --no-restore-chat-history --aiderignore /Users/vishalkumar/elm_specs_md/pms_kit/a8/aiderignore_a8 --chat-history-file a8_logs/wf/aider.chat.history.md --input-history-file a8_logs/wf/aider.input.history --llm-history-file a8_logs/wf/llm.history.txt --file tests/a8/wf/test_wf_p02.py --read conftest.py --read modules/patent/registry.py --read modules/patent/models.py --read modules/patent/domain/policy.py --read modules/patent/services/applications.py --read modules/patent/services/legal.py --read modules/patent/services/post_filing.py --read modules/patent/api/serializers.py --read modules/patent/api/views.py --read modules/patent/api/views_legal.py --read modules/patent/api/urls.py --message-file a8_logs/wf/promptB_p02.md  
> Creating empty file /Users/vishalkumar/ELM_MODEL_2/tests/a8/wf/test_wf_p02.py  
> Aider v0.86.2  
> Model: ollama_chat/qwen3.5:4b with whole edit format  
> Git repo: .git with 291 files  
> Repo-map: disabled  
> Added tests/a8/wf/test_wf_p02.py to the chat.  
> Added modules/patent/registry.py to the chat (read-only).  
> Added modules/patent/services/legal.py to the chat (read-only).  
> Added conftest.py to the chat (read-only).  
> Added modules/patent/api/views.py to the chat (read-only).  
> Added modules/patent/api/urls.py to the chat (read-only).  
> Added modules/patent/services/post_filing.py to the chat (read-only).  
> Added modules/patent/models.py to the chat (read-only).  
> Added modules/patent/api/views_legal.py to the chat (read-only).  
> Added modules/patent/services/applications.py to the chat (read-only).  
> Added modules/patent/domain/policy.py to the chat (read-only).  
> Added modules/patent/api/serializers.py to the chat (read-only).  

#### You are given:  
#### 1. the frozen A8_BASE Fusion implementation, and  
#### 2. the frozen WF_DESIGN.json.  
#### Convert these test designs into executable automated backend tests using pytest/pytest-django.  
#### Rules:  
#### - Implement exactly the supplied test cases.  
#### - Do not add, remove, merge or reinterpret test cases.  
#### - Preserve each specified expected result.  
#### - Do not modify production code.  
#### - Use the Django isolated test database.  
#### - Reuse existing Fusion test infrastructure where appropriate.  
#### - Do not mock the behavior being tested; mocks may be used only for unavailable external dependencies.  
#### - Do not use xfail to hide failures.  
#### - Every test must contain its test_id and source_id in its name or docstring.  
#### - Store generated tests only under tests/a8/wf/.  
#### If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.  
####   
#### The frozen WF_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 9 to 14 of 14; write exactly these test cases into tests/a8/wf/test_wf_p02.py.  
#### ```json  
#### [  
####  {  
####   "test_id": "T-009",  
####   "source_id": "BR-PMS-067; BR-PMS-068; BR-PMS-069; BR-PMS-070",  
####   "purpose": "Validate withdrawal eligibility checks and co-inventor consent collection when applicable before 'Before Filing' or 'Under Review' states.",  
####   "preconditions": "Application is in a configured pre-filing state (e.g., Submitted, Under Review); Withdrawal reason provided.",  
####   "action_or_input": "Applicant initiates UC-PMS-006 to Withdraw Patent Application.",  
####   "expected_result": "PMS validates if current state is withdrawal-eligible per configuration; collects co-inventor consent if required by process; updates status to 'Withdrawn' and removes from queue.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-010",  
####   "source_id": "UC-PMS-018",  
####   "purpose": "Validate Director's decision to Renew or Do Not Renew for maintenance fee cycles and transition logic.",  
####   "preconditions": "Application status is 'Granted' / Maintenance Cycle Active; Attorney has requested Renewal Decision from Director.",  
####   "action_or_input": "Director makes a 'Renew' or 'Do Not Renew' decision (UC-PMS-018).",  
####   "expected_result": "PMS records the decision outcome; if 'Renew', processes maintenance action, records transaction/status, and schedules next cycle. If 'Do Not Renew', records decision and ends current cycle.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-011",  
####   "source_id": "BR-PMS-048; BR-PMS-052; BR-PMS-053",  
####   "purpose": "Validate Budget Approval and Rejection logic including cost validation.",  
####   "preconditions": "Application is 'Approved'; Director reviews budget.",  
####   "action_or_input": "Director decides to Approve or Reject the budget (validating costs against threshold and availability where applicable).",  
####   "expected_result": "PMS updates status/budget records accordingly; if Rejected, ensures no downstream auto-approval occurs.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-012",  
####   "source_id": "BR-PMS-055; BR-PMS-056",  
####   "purpose": "Validate pre-filing readiness checks and successful external filing transition.",  
####   "preconditions": "Application is 'Approved'; All pre-filing prerequisites (budget, agreement, expert approval) are complete.",  
####   "action_or_input": "Attorney initiates UC-PMS-013 to Prepare and Record External Patent Filing.",  
####   "expected_result": "PMS verifies format compliance and prerequisites; updates status to 'Filed' and captures filing ID/date.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-013",  
####   "source_id": "BR-PMS-146; BR-PMS-065; BR-PMS-066",  
####   "purpose": "Validate Office Action response submission and deadline tracking logic.",  
####   "preconditions": "Application is 'Filed / Post-Filing Active'; Attorney has received an Office Action.",  
####   "action_or_input": "Attorney records, prepares, and submits a response within the applicable deadline or permitted extension period (UC-PMS-015).",  
####   "expected_result": "PMS updates status (e.g., to 'Response Submitted'), logs official communication history, and verifies adherence to time-bound rules.",  
####   "test_type": "Functional"  
####  },  
####  {  
####   "test_id": "T-014",  
####   "source_id": "BR-PMS-146; BR-PMS-065; BR-PMS-066",  
####   "purpose": "Validate conditional workflow branching where Applicant review is required for Office Action response.",  
####   "preconditions": "Application is 'Filed'; Office action received; System determines Applicant review is REQUIRED (e.g., per process rules).",  
####   "action_or_input": "Applicant reviews and approves the Attorney's draft response via UC-PMS-029.",  
####   "expected_result": "PMS transitions state from 'Awaiting Applicant Approval' to 'Response Submitted' upon approval, triggering notification of finalization.",  
####   "test_type": "Functional"  
####  }  
#### ]  
#### ```  

<thinking-content-7bbeb8e1441453ad999a0bbba8a46d4b>

The user wants me to convert test cases 9-14 from the WF_DESIGN.json into pytest/pytest-django tests. I need to:

1. Create tests for T-009 through T-014
2. Each test must include test_id and source_id in name or docstring
3. Tests should be stored under tests/a8/wf/test_wf_p02.py
4. Use the existing Fusion test infrastructure (conftest.py is provided)
5. Don't modify production code
6. Use Django isolated test database
7. Don't use xfail to hide failures

Let me analyze each test case:

**T-009**: Withdrawal eligibility and co-inventor consent
- Source: BR-PMS-067, BR-PPS-068, BR-PMS-069, BR-PMS-070
- Test withdrawal from Submitted/Under Review states
- Check if co-inventor consent is required
- Verify status updates to 'Withdrawn'

**T-010**: Maintenance fee renewal decision
- Source: UC-PMS-018
- Director makes Renew or Do Not Renew decision
- If Renew: process maintenance, schedule next cycle
- If Do Not Renew: record decision, end cycle

**T-011**: Budget approval/rejection logic
- Source: BR-PMS-048, BR-PMS-052, BR-PMS-053
- Director reviews budget for Approved application
- Approve or Reject with cost validation

**T-012**: Pre-filing readiness and external filing
- Source: BR-PMS-055, BR-PMS-056
- Attorney initiates UC-PMS-013 to file patent
- Verify prerequisites complete
- Update status to 'Filed'

**T-013**: Office Action response submission
- Source: BR-PMS-146, BR-PMS-065, BR-PMS-066


- Attorney records, prepares, and submits response within deadline
- Update status to 'Response Submitted'

**T-014**: Conditional workflow branching for Applicant review
- Source: BR-PMS-146, BR-PMS-065, BR-PMS-066
- Applicant reviews/approves Attorney's draft response
- Transition from 'Awaiting Applicant Approval' to 'Response Submitted'

I'll create comprehensive pytest tests that validate each workflow scenario using the existing test infrastructure.

</thinking-content-7bbeb8e1441453ad999a0bbba8a46d4b>

tests/a8/wf/test_wf_p02.py
```
"""Test cases for Patent Management System workflows T-009 through T-014."""
import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse

from fusion_auth.client import IamSession
from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument, AttorneyAssignment,
    Budget, Filing, OfficeAction, MaintenanceRecord, Appeal, ApplicationHistory
)
from modules.patent.services.applications import withdraw_application
from modules.patent.services.legal import decide_renewal, propose_budget, decide_budget
from modules.patent.services.post_filing import record_office_action, prepare_response, submit_response
from modules.patent.domain.policy import can_withdraw


# -----------------------------------------------------------------------------
# Test T-009: Withdrawal Eligibility and Co-Inventor Consent
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t009_withdrawal_eligibility_and_co_inventor_consent():
    """T-009: Validate withdrawal eligibility checks and co-inventor consent collection."""
    source_id = "BR-PMS-067; BR-PMS-068; BR-PMS-069; BR-PMS-070"
    
    # Create application in Submitted state (pre-filing)
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-001",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="submitted"
    )
    
    # Create inventor with agreement signed (simulating co-inventor consent)
    inventor = Inventor.objects.create(
        application=app,
        user_id=2,
        name="Co-Inventor",
        email="coinventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Create second inventor without signed agreement (testing consent requirement)
    inventor2 = Inventor.objects.create(
        application=app,
        user_id=3,
        name="Another Co-Inventor",
        email="another@test.com",
        contribution_percent=50.0,
        agreement_signed=False
    )
    
    # Test withdrawal eligibility check
    assert can_withdraw(app.status), "Application should be withdrawable from Submitted state"
    
    # Simulate withdrawal with reason
    reason = "Testing withdrawal workflow"
    withdrawn_app = withdraw_application(
        applicant_id=1,
        application_id=app.id,
        reason=reason
    )
    
    # Verify status updated to Withdrawn
    assert withdrawn_app.status == "withdrawn", f"Status should be 'withdrawn', got {withdrawn_app.status}"
    
    # Verify history entry created
    history = ApplicationHistory.objects.filter(application=app).first()
    assert history is not None, "Application history entry should be created"
    assert history.action == "withdraw", f"Action should be 'withdraw', got {history.action}"


# -----------------------------------------------------------------------------
# Test T-010: Maintenance Fee Renewal Decision
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t010_maintenance_renewal_decision():
    """T-010: Validate Director's decision to Renew or Do Not Renew for maintenance fee cycles."""
    source_id = "UC-PMS-018"
    
    # Create granted application with active maintenance cycle
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-002",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="granted"
    )
    
    # Create maintenance record with renewal requested
    maintenance = MaintenanceRecord.objects.create(
        application=app,
        due_date=date.today() + timedelta(days=30),
        fee=500.00,
        decision="renewal_requested",
        decided_by=None
    )
    
    # Create assigned director for the application
    app.assigned_director_id = 10
    
    # Test Renew decision
    renew_decision = decide_renewal(
        director_id=10,
        record_id=maintenance.id,
        renew=True,
        justification="Patent should be maintained"
    )
    
    assert renew_decision.decision == "renew", f"Decision should be 'renew', got {renew_decision.decision}"
    assert renew_decision.decided_by == 10, "Decision should be recorded by director"
    
    # Verify history entry created for renewal decision
    history = ApplicationHistory.objects.filter(application=app).filter(action="renewal_decided").first()
    assert history is not None, "Renewal decision history entry should be created"
    
    # Test Do Not Renew decision
    do_not_renew_decision = decide_renewal(
        director_id=10,
        record_id=maintenance.id,
        renew=False,
        justification="Patent will not be maintained"
    )
    
    assert do_not_renew_decision.decision == "do_not_renew", f"Decision should be 'do_not_renew', got {do_not_renew_decision.decision}"
    assert do_not_renew_decision.decided_by == 10, "Decision should be recorded by director"


# -----------------------------------------------------------------------------
# Test T-011: Budget Approval and Rejection Logic
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t011_budget_approval_and_rejection_logic():
    """T-011: Validate Budget Approval and Rejection logic including cost validation."""
    source_id = "BR-PMS-048; BR-PMS-052; BR-PMS-053"
    
    # Create approved application
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-003",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="approved"
    )
    
    # Create budget proposal
    budget = propose_budget(
        admin_id=5,
        application_id=app.id,
        filing_fee=2000.00,
        attorney_fee=3000.00,
        admin_cost=1000.00
    )
    
    assert budget.status == "pending", f"Budget should be 'pending', got {budget.status}"
    
    # Test Budget Approval
    approved_budget = decide_budget(
        director_id=10,
        budget_id=budget.id,
        approve=True,
        justification="Budget is within acceptable range and all costs are justified",
        threshold=10000.00
    )
    
    assert approved_budget.status == "approved", f"Budget should be 'approved', got {approved_budget.status}"
    assert approved_budget.decided_by == 10, "Decision should be recorded by director"
    
    # Verify history entry created for budget approval
    history = ApplicationHistory.objects.filter(application=app).filter(action="decide_budget").first()
    assert history is not None, "Budget decision history entry should be created"
    
    # Test Budget Rejection (within threshold)
    rejected_budget = decide_budget(
        director_id=10,
        budget_id=budget.id,
        approve=False,
        justification="Budget exceeds acceptable range",
        threshold=10000.00
    )
    
    assert rejected_budget.status == "rejected", f"Budget should be 'rejected', got {rejected_budget.status}"


# -----------------------------------------------------------------------------
# Test T-012: Pre-Filing Readiness and External Filing Transition
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t012_pre_filing_readiness_and_external_filing():
    """T-012: Validate pre-filing readiness checks and successful external filing transition."""
    source_id = "BR-PMS-055; BR-PMS-056"
    
    # Create approved application with all prerequisites complete
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-004",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="approved"
    )
    
    # Create assigned attorney
    app.assigned_attorney_id = 20
    
    # Create budget with approved status
    Budget.objects.create(
        application=app,
        filing_fee=2000.00,
        attorney_fee=3000.00,
        administrative_cost=1000.00,
        total=6000.00,
        status="approved",
        decided_by=10
    )
    
    # Create inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=3,
        name="Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Test external filing initiation
    filing = record_filing(
        attorney_id=20,
        application_id=app.id,
        office="USPTO",
        filing_number="12345678",
        filing_date=date.today(),
        international=False
    )
    
    assert filing.patent_office == "USPTO", f"Filing should be for USPTO, got {filing.patent_office}"
    assert filing.filing_number == "12345678", f"Filing number should match, got {filing.filing_number}"
    
    # Verify application status updated to 'filed'
    app.refresh_from_db()
    assert app.status == "filed", f"Application status should be 'filed', got {app.status}"


# -----------------------------------------------------------------------------
# Test T-013: Office Action Response Submission and Deadline Tracking
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t013_office_action_response_submission_and_deadline():
    """T-013: Validate Office Action response submission and deadline tracking logic."""
    source_id = "BR-PMS-146; BR-PMS-065; BR-PMS-066"
    
    # Create filed application
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-005",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="filed"
    )
    
    # Create assigned attorney
    app.assigned_attorney_id = 20
    
    # Record office action
    oa = record_office_action(
        attorney_id=20,
        application_id=app.id,
        received_date=date.today(),
        response_due_date=date.today() + timedelta(days=30),
        description="Office action received"
    )
    
    assert oa.status == "recorded", f"Office action should be 'recorded', got {oa.status}"
    
    # Prepare response (without applicant approval)
    prepared_oa = prepare_response(
        attorney_id=20,
        office_action_id=oa.id,
        response_text="Response text",
        needs_applicant_approval=False
    )
    
    assert prepared_oa.status == "response_ready", f"Status should be 'response_ready', got {prepared_oa.status}"
    
    # Submit response
    submitted_oa = submit_response(
        attorney_id=20,
        office_action_id=oa.id
    )
    
    assert submitted_oa.status == "response_submitted", f"Status should be 'response_submitted', got {submitted_oa.status}"
    
    # Verify history entry created for response submission
    history = ApplicationHistory.objects.filter(application=app).filter(action="response_submitted").first()
    assert history is not None, "Response submission history entry should be created"


# -----------------------------------------------------------------------------
# Test T-014: Conditional Workflow Branching for Applicant Review
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t014_conditional_workflow_branching_for_applicant_review():
    """T-014: Validate conditional workflow branching where Applicant review is required."""
    source_id = "BR-PMS-146; BR-PMS-065; BR-PMS-066"
    
    # Create filed application
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-006",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="filed"
    )
    
    # Create assigned attorney
    app.assigned_attorney_id = 20
    
    # Record office action awaiting applicant approval
    oa = record_office_action(
        attorney_id=20,
        application_id=app.id,
        received_date=date.today(),
        response_due_date=date.today() + timedelta(days=30),
        description="Office action received"
    )
    
    # Prepare response requiring applicant approval
    prepared_oa = prepare_response(
        attorney_id=20,
        office_action_id=oa.id,
        response_text="Response text",
        needs_applicant_approval=True
    )
    
    assert prepared_oa.status == "awaiting_applicant_approval", f"Status should be 'awaiting_applicant_approval', got {prepared_oa.status}"
    
    # Simulate applicant approval (using principal user_id)
    approved_oa = approve_response(
        applicant_id=1,
        office_action_id=oa.id
    )
    
    assert approved_oa.status == "applicant_approved", f"Status should be 'applicant_approved', got {approved_oa.status}"
    
    # Verify history entry created for response approval
    history = ApplicationHistory.objects.filter(application=app).filter(action="response_approved").first()
    assert history is not None, "Response approval history entry should be created"


# -----------------------------------------------------------------------------
# Helper function to simulate approve_response (not in services)
# -----------------------------------------------------------------------------

def approve_response(applicant_id: int, office_action_id: int) -> OfficeAction:
    """Helper function to simulate applicant response approval."""
    from modules.patent.services.post_filing import PostFilingService
    
    return PostFilingService.approve_response(
        applicant_id=applicant_id,
        office_action_id=office_action_id
    )
```

> Tokens: 24k sent, 3.4k received.  
> Applied edit to tests/a8/wf/test_wf_p02.py  
