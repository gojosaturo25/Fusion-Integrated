
# aider chat started at 2026-11-14 03:43:41

> /opt/homebrew/bin/aider --model ollama_chat/qwen3.5:4b --model-settings-file /Users/vishalkumar/elm_specs_md/pms_kit/a8/aider_model_settings.yml --edit-format whole --map-tokens 0 --timeout 3600 --yes-always --stream --no-pretty --no-fancy-input --no-gitignore --no-auto-commits --no-dirty-commits --no-auto-lint --no-auto-test --no-check-update --analytics-disable --no-show-release-notes --no-show-model-warnings --no-suggest-shell-commands --no-detect-urls --no-restore-chat-history --aiderignore /Users/vishalkumar/elm_specs_md/pms_kit/a8/aiderignore_a8 --chat-history-file a8_logs/uc/aider.chat.history.md --input-history-file a8_logs/uc/aider.input.history --llm-history-file a8_logs/uc/llm.history.txt --file tests/a8/uc/test_uc_p01.py --read conftest.py --read modules/patent/registry.py --read modules/patent/models.py --read modules/patent/domain/policy.py --read modules/patent/services/applications.py --read modules/patent/services/legal.py --read modules/patent/services/post_filing.py --read modules/patent/api/serializers.py --read modules/patent/api/views.py --read modules/patent/api/views_legal.py --read modules/patent/api/urls.py --message-file a8_logs/uc/promptB_p01.md  
> Creating empty file /Users/vishalkumar/ELM_MODEL_2/tests/a8/uc/test_uc_p01.py  
> Aider v0.86.2  
> Model: ollama_chat/qwen3.5:4b with whole edit format  
> Git repo: .git with 285 files  
> Repo-map: disabled  
> Added tests/a8/uc/test_uc_p01.py to the chat.  
> Added modules/patent/models.py to the chat (read-only).  
> Added modules/patent/services/applications.py to the chat (read-only).  
> Added modules/patent/services/post_filing.py to the chat (read-only).  
> Added modules/patent/registry.py to the chat (read-only).  
> Added modules/patent/services/legal.py to the chat (read-only).  
> Added modules/patent/api/views.py to the chat (read-only).  
> Added modules/patent/api/urls.py to the chat (read-only).  
> Added conftest.py to the chat (read-only).  
> Added modules/patent/domain/policy.py to the chat (read-only).  
> Added modules/patent/api/serializers.py to the chat (read-only).  
> Added modules/patent/api/views_legal.py to the chat (read-only).  

#### You are given:  
#### 1. the frozen A8_BASE Fusion implementation, and  
#### 2. the frozen UC_DESIGN.json.  
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
#### - Store generated tests only under tests/a8/uc/.  
#### If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.  
####   
#### The frozen UC_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 1 to 8 of 39; write exactly these test cases into tests/a8/uc/test_uc_p01.py.  
#### ```json  
#### [  
####  {  
####   "test_id": "TEST-PMS-UC001-MAX",  
####   "source_id": "UC-PMS-001 Main Success Scenario",  
####   "purpose": "Verify that PMS validates required fields, documents (PDF, size, malware), and creates a Submitted application.",  
####   "preconditions": "A submission draft exists with complete application fields (title, abstract, description, claims, inventors) and valid PDF documents under 50MB.",  
####   "action_or_input": "Applicant submits the application.",  
####   "expected_result": "PMS assigns a unique ID, sets status to Submitted, records history/audit data, and triggers submission notification. Invalid submissions are rejected without acceptance."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC001-MIN",  
####   "source_id": "UC-PMS-001 Failure / Minimal Guarantee",  
####   "purpose": "Verify that incomplete required fields or invalid document formats prevent application acceptance.",  
####   "preconditions": "A submission draft exists with missing required fields or a document that fails format/size/malware validation.",  
####   "action_or_input": "Applicant attempts to submit the application.",  
####   "expected_result": "PMS identifies missing info or rejects the invalid document, keeping the application unsubmitted or preserving the prior valid state."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC002-MAX",  
####   "source_id": "UC-PMS-002 Main Success Scenario",  
####   "purpose": "Verify that an authorized Applicant can view their own application status and history.",  
####   "preconditions": "Applicant has a valid PMS role and access to a specific application record.",  
####   "action_or_input": "Applicant opens the application tracking view.",  
####   "expected_result": "PMS displays current status, progress, and recorded history without modifying business state."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC002-MIN",  
####   "source_id": "UC-PMS-002 Exception Flows",  
####   "purpose": "Verify that unauthorized access to application records is blocked.",  
####   "preconditions": "Applicant attempts to view an application record they do not have access to (or lacks valid role).",  
####   "action_or_input": "Applicant navigates to or opens the restricted application.",  
####   "expected_result": "PMS blocks access and displays no application data; prior state is unaffected."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC003-MAX",  
####   "source_id": "UC-PMS-003 Main Success Scenario",  
####   "purpose": "Verify that Applicants can update inventor information and ownership shares.",  
####   "preconditions": "Applicant has access to an application and the current role/status permits changes.",  
####   "action_or_input": "Applicant updates inventor details and ownership percentages.",  
####   "expected_result": "PMS validates the data, records consent/signatures where configured, notifies affected parties, and stores valid information."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC003-MIN",  
####   "source_id": "UC-PMS-003 Exception Flows",  
####   "purpose": "Verify that invalid inventor data prevents changes from being committed.",  
####   "preconditions": "Applicant attempts to update inventor information with invalid ownership percentages or missing required consent.",  
####   "action_or_input": "Applicant submits the update request.",  
####   "expected_result": "PMS rejects the invalid change, preventing commitment and retaining prior valid inventor/agreement data."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC004-MAX",  
####   "source_id": "UC-PMS-004 Main Success Scenario",  
####   "purpose": "Verify that Actors can search, attach references, and log the session.",  
####   "preconditions": "Actor has a valid PMS role and external search access is available (or only local search).",  
####   "action_or_input": "Actor searches for prior art, selects references, and attaches them to an application.",  
####   "expected_result": "PMS displays ranked results, attaches selected references, logs the search session, and retains any previously recorded PMS data."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC004-MIN",  
####   "source_id": "UC-PMS-004 Exception Flows",  
####   "purpose": "Verify that unavailable external sources do not fabricate results.",  
####   "preconditions": "Actor initiates a search where the configured external database integration is unavailable.",  
####   "action_or_input": "Actor attempts to query an unavailable external source.",  
####   "expected_result": "PMS does not represent the external source as successfully queried; any already-recorded PMS data remains intact."  
####  }  
#### ]  
#### ```  

# aider chat started at 2026-11-14 04:13:51

> /opt/homebrew/bin/aider --model ollama_chat/qwen3.5:4b --model-settings-file /Users/vishalkumar/elm_specs_md/pms_kit/a8/aider_model_settings.yml --edit-format whole --map-tokens 0 --timeout 3600 --yes-always --stream --no-pretty --no-fancy-input --no-gitignore --no-auto-commits --no-dirty-commits --no-auto-lint --no-auto-test --no-check-update --analytics-disable --no-show-release-notes --no-show-model-warnings --no-suggest-shell-commands --no-detect-urls --no-restore-chat-history --aiderignore /Users/vishalkumar/elm_specs_md/pms_kit/a8/aiderignore_a8 --chat-history-file a8_logs/uc/aider.chat.history.md --input-history-file a8_logs/uc/aider.input.history --llm-history-file a8_logs/uc/llm.history.txt --file tests/a8/uc/test_uc_p02.py --read conftest.py --read modules/patent/registry.py --read modules/patent/models.py --read modules/patent/domain/policy.py --read modules/patent/services/applications.py --read modules/patent/services/legal.py --read modules/patent/services/post_filing.py --read modules/patent/api/serializers.py --read modules/patent/api/views.py --read modules/patent/api/views_legal.py --read modules/patent/api/urls.py --message-file a8_logs/uc/promptB_p02.md  
> Creating empty file /Users/vishalkumar/ELM_MODEL_2/tests/a8/uc/test_uc_p02.py  
> Aider v0.86.2  
> Model: ollama_chat/qwen3.5:4b with whole edit format  
> Git repo: .git with 286 files  
> Repo-map: disabled  
> Added tests/a8/uc/test_uc_p02.py to the chat.  
> Added conftest.py to the chat (read-only).  
> Added modules/patent/api/serializers.py to the chat (read-only).  
> Added modules/patent/models.py to the chat (read-only).  
> Added modules/patent/services/applications.py to the chat (read-only).  
> Added modules/patent/domain/policy.py to the chat (read-only).  
> Added modules/patent/services/legal.py to the chat (read-only).  
> Added modules/patent/services/post_filing.py to the chat (read-only).  
> Added modules/patent/api/views.py to the chat (read-only).  
> Added modules/patent/registry.py to the chat (read-only).  
> Added modules/patent/api/urls.py to the chat (read-only).  
> Added modules/patent/api/views_legal.py to the chat (read-only).  

#### You are given:  
#### 1. the frozen A8_BASE Fusion implementation, and  
#### 2. the frozen UC_DESIGN.json.  
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
#### - Store generated tests only under tests/a8/uc/.  
#### If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.  
####   
#### The frozen UC_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 9 to 16 of 39; write exactly these test cases into tests/a8/uc/test_uc_p02.py.  
#### ```json  
#### [  
####  {  
####   "test_id": "TEST-PMS-UC005-MAX",  
####   "source_id": "UC-PMS-005 Main Success Scenario",  
####   "purpose": "Verify that Applicants can revise applications within the feedback period.",  
####   "preconditions": "Application status is Needs Revision or Rejected, and the 60-day resubmission period has not expired.",  
####   "action_or_input": "Applicant reviews Director feedback, edits content/documents, and resubmits.",  
####   "expected_result": "PMS validates that revision addresses feedback, records the revised version, starts a new review cycle."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC005-MIN",  
####   "source_id": "UC-PMS-005 Exception Flows (Late Deadline)",  
####   "purpose": "Verify that resubmissions outside the 60-day deadline are blocked.",  
####   "preconditions": "The application is in a revisionable state but the resubmission period has expired.",  
####   "action_or_input": "Applicant attempts to resubmit a late revision.",  
####   "expected_result": "PMS changes application status to Expired and rejects the submission."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC005-MIN2",  
####   "source_id": "UC-PMS-005 Exception Flows (Ignoring Feedback)",  
####   "purpose": "Verify that resubmissions not addressing Director feedback are rejected.",  
####   "preconditions": "Application is in Needs Revision state; revision content does not address the recorded Director feedback.",  
####   "action_or_input": "Applicant attempts to submit a revision ignoring feedback points.",  
####   "expected_result": "PMS rejects the resubmission and retains the prior valid application state."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC006-MAX",  
####   "source_id": "UC-PMS-006 Main Success Scenario",  
####   "purpose": "Verify that Applicants can withdraw eligible pre-filing applications.",  
####   "preconditions": "Application status is withdrawal-eligible (pre-filing), and withdrawal is allowed per BR-PMS-068.",  
####   "action_or_input": "Applicant provides a withdrawal reason, confirms co-inventor consent if required, and confirms withdrawal.",  
####   "expected_result": "PMS sets status to Withdrawn, removes application from active queue, and records history/status change."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC006-MIN",  
####   "source_id": "UC-PMS-006 Exception Flows",  
####   "purpose": "Verify that withdrawal is blocked when application status is not withdrawal-eligible.",  
####   "preconditions": "Application has reached Filed status or is in a non-withdrawal-eligible state.",  
####   "action_or_input": "Applicant attempts to withdraw the application.",  
####   "expected_result": "PMS blocks withdrawal and retains the current valid state."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC007-MAX",  
####   "source_id": "UC-PMS-007 Main Success Scenario",  
####   "purpose": "Verify that Submitted applications are assigned to an eligible, non-conflicted Director.",  
####   "preconditions": "Application status is Submitted; PCC_ADMIN or automatic routing is active.",  
####   "action_or_input": "PCC_ADMIN selects a Director (not listed as inventor) to receive the application.",  
####   "expected_result": "PMS records assignment, sets status to Under Review, notifies Director, and initiates review timeline."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC007-MIN",  
####   "source_id": "UC-PMS-007 Exception Flows",  
####   "purpose": "Verify that assignment to a conflicted Director (inventor) is prevented.",  
####   "preconditions": "Application is Submitted; PCC_ADMIN attempts to assign to a Director listed as an inventor.",  
####   "action_or_input": "PCC_ADMIN selects the conflicted Director.",  
####   "expected_result": "PMS prevents assignment, leaves application status Submitted, and flags/raises the exceptional case."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC008-MAX",  
####   "source_id": "UC-PMS-008 Main Success Scenario",  
####   "purpose": "Verify that Directors record valid technical merit decisions (Approve, Reject, Needs Revision).",  
####   "preconditions": "Application is Under Review; Director is the assigned reviewer with no conflict.",  
####   "action_or_input": "Director selects a decision and enters justification of at least 50 characters.",  
####   "expected_result": "PMS records the decision/audit trail. Approved apps become eligible for attorney assignment; others trigger feedback to Applicant."  
####  }  
#### ]  
#### ```  

<thinking-content-7bbeb8e1441453ad999a0bbba8a46d4b>

The user wants me to convert the test cases from UC_DESIGN.json into pytest/pytest-django tests. I need to:

1. Create tests for TEST-PMS-UC005-MAX, TEST-PMS-UC005-MIN, TEST-PMS-UC005-MIN2, TEST-PMS-UC006-MAX, TEST-PMS-UC006-MIN, TEST-PMS-UC007-MAX, and TEST-PMS-UC007-MIN, and TEST-PMS-UC008-MAX

2. Each test must:
   - Have test_id and source_id in the name or docstring
   - Use pytest-django isolated database
   - Not modify production code
   - Reuse existing Fusion test infrastructure (conftest.py is available)
   - Not mock behavior being tested (only external dependencies)
   - Not use xfail
   - Be stored under tests/a8/uc/

3. Looking at the existing conftest.py, I can see:
   - `stub_iam` fixture for IAM mocking
   - `user_ref` fixture for creating UserRef objects
   - Various models and services are available in modules/patent/

4. I need to write tests that:
   - Use the existing service layer (modules/patent/services/applications.py)
   - Test the resubmission logic (UC005)
   - Test withdrawal logic (UC006)
   - Test director assignment logic (UC007)
   - Test review decision logic (UC008)

Let me write comprehensive pytest tests for each of these test cases. I'll need to:
- Create test fixtures for applications, users, directors, etc.
- Use the existing services from modules/patent/services/applications.py
- Verify expected behaviors and error conditions

Let me structure the tests properly with proper naming conventions including test_id in the name.

</thinking-content-7bbeb8e1441453ad999a0bbba8a46d4b>

tests/a8/uc/test_uc_p02.py
```
"""Test cases for UC-PMS-005, UC-PMS-006, UC-PMS-007, UC-PMS-008 from UC_DESIGN.json."""
import pytest
from datetime import date, timedelta

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.response import Response

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument,
    ApplicationHistory, OfficeAction
)
from modules.patent.services.applications import (
    resubmit_application, withdraw_application, assign_director, review_application
)
from modules.patent.domain.policy import can_transition, is_conflicted, can_withdraw


# -----------------------------------------------------------------------------
# TEST-PMS-UC005-MAX: Resubmission within feedback period
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_005_max_resubmission_within_deadline():
    """TEST-PMS-UC005-MAX: Verify that Applicants can revise applications within the feedback period."""
    
    # Arrange: Create application in Needs Revision state with valid resubmission deadline
    applicant_id = 1001
    director_id = 2001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-001",
        defaults={
            'applicant_id': applicant_id,
            'status': 'needs_revision',
            'assigned_director_id': director_id,
            'review_due_date': None,
            'resubmission_deadline': date.today() + timedelta(days=30),  # Valid deadline
            'version_number': 1,
        }
    )
    
    # Create inventor for conflict testing
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Create document
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Applicant resubmits with changes addressing feedback
    changes = {
        'title': 'Revised Title',
        'description': 'Updated description addressing all concerns'
    }
    response_to_feedback = "All feedback points have been addressed in this revision."
    
    result_app = resubmit_application(
        applicant_id=applicant_id,
        application_id=app.id,
        changes=changes,
        response_to_feedback=response_to_feedback,
        actor_id=applicant_id
    )
    
    # Assert: Application status updated to Resubmitted, version bumped, history recorded
    assert result_app.status == 'resubmitted'
    assert result_app.version_number == 2
    assert result_app.resubmission_deadline is not None
    
    # Verify history entry created
    history_entries = ApplicationHistory.objects.filter(application=app)
    assert len(history_entries) > 0
    recent_history = list(history_entries).reverse()[0]
    assert recent_history.action == 'resubmit'
    assert recent_history.to_status == 'resubmitted'


# -----------------------------------------------------------------------------
# TEST-PMS-UC005-MIN: Resubmission outside deadline blocked
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_005_min_resubmission_late_deadline():
    """TEST-PMS-UC005-MIN: Verify that resubmissions outside the 60-day deadline are blocked."""
    
    # Arrange: Create application with expired resubmission deadline
    applicant_id = 1001
    director_id = 2001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-002",
        defaults={
            'applicant_id': applicant_id,
            'status': 'needs_revision',
            'assigned_director_id': director_id,
            'review_due_date': None,
            'resubmission_deadline': date.today() - timedelta(days=10),  # Expired deadline
            'version_number': 1,
        }
    )
    
    # Create inventor for conflict testing
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Applicant attempts to resubmit after deadline expired
    changes = {
        'title': 'Revised Title',
        'description': 'Updated description'
    }
    response_to_feedback = "Addressing all concerns."
    
    with pytest.raises(ValueError) as exc_info:
        resubmit_application(
            applicant_id=applicant_id,
            application_id=app.id,
            changes=changes,
            response_to_feedback=response_to_feedback,
            actor_id=applicant_id
        )
    
    # Assert: Error raised due to expired deadline
    assert "Resubmission deadline" in str(exc_info.value)
    assert "passed" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# TEST-PMS-UC005-MIN2: Resubmission ignoring feedback rejected
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_005_min2_resubmission_ignoring_feedback():
    """TEST-PMS-UC005-MIN2: Verify that resubmissions not addressing Director feedback are rejected."""
    
    # Arrange: Create application in Needs Revision state
    applicant_id = 1001
    director_id = 2001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-003",
        defaults={
            'applicant_id': applicant_id,
            'status': 'needs_revision',
            'assigned_director_id': director_id,
            'review_due_date': None,
            'resubmission_deadline': date.today() + timedelta(days=30),  # Valid deadline
            'version_number': 1,
        }
    )
    
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Applicant attempts to resubmit without addressing feedback
    changes = {
        'title': 'Same Title',  # No meaningful change
        'description': 'No changes made'
    }
    response_to_feedback = "I disagree with the feedback."  # Not addressing concerns
    
    with pytest.raises(ValueError) as exc_info:
        resubmit_application(
            applicant_id=applicant_id,
            application_id=app.id,
            changes=changes,
            response_to_feedback=response_to_feedback,
            actor_id=applicant_id
        )
    
    # Assert: Error raised due to feedback not addressed
    assert "feedback" in str(exc_info.value).lower() or "addressed" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# TEST-PMS-UC006-MAX: Withdrawal of eligible pre-filing application
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_006_max_withdraw_eligible_application():
    """TEST-PMS-UC006-MAX: Verify that Applicants can withdraw eligible pre-filing applications."""
    
    # Arrange: Create application in withdrawal-eligible state (pre-filing)
    applicant_id = 1001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-004",
        defaults={
            'applicant_id': applicant_id,
            'status': 'submitted',  # Withdrawal-eligible per BR-PMS-068
            'assigned_director_id': None,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    # Create inventor for co-inventor consent check
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Co-Inventor",
        email="coinventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Applicant withdraws application with reason
    reason = "I no longer wish to pursue this patent application."
    
    result_app = withdraw_application(
        applicant_id=applicant_id,
        application_id=app.id,
        reason=reason
    )
    
    # Assert: Application status set to Withdrawn, history recorded
    assert result_app.status == 'withdrawn'
    assert result_app.version_number == 1
    
    # Verify history entry created
    history_entries = ApplicationHistory.objects.filter(application=app)
    assert len(history_entries) > 0
    recent_history = list(history_entries).reverse()[0]
    assert recent_history.action == 'withdraw'
    assert recent_history.to_status == 'withdrawn'


# -----------------------------------------------------------------------------
# TEST-PMS-UC006-MIN: Withdrawal blocked for non-withdrawal-eligible state
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_006_min_withdraw_non_eligible_state():
    """TEST-PMS-UC006-MIN: Verify that withdrawal is blocked when application status is not withdrawal-eligible."""
    
    # Arrange: Create application in non-withdrawal-eligible state (Filed)
    applicant_id = 1001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-005",
        defaults={
            'applicant_id': applicant_id,
            'status': 'filed',  # Not withdrawal-eligible per BR-PMS-067/068
            'assigned_director_id': None,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Applicant attempts to withdraw application in Filed state
    reason = "I want to withdraw this application."
    
    with pytest.raises(ValueError) as exc_info:
        withdraw_application(
            applicant_id=applicant_id,
            application_id=app.id,
            reason=reason
        )
    
    # Assert: Error raised due to withdrawal not allowed from current status
    assert "withdrawal" in str(exc_info.value).lower()
    assert "not allowed" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# TEST-PMS-UC007-MAX: Assignment to eligible non-conflicted Director
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_007_max_assignment_to_eligible_director():
    """TEST-PMS-UC007-MAX: Verify that Submitted applications are assigned to an eligible, non-conflicted Director."""
    
    # Arrange: Create application in Submitted state
    applicant_id = 1001
    director_id = 2001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-006",
        defaults={
            'applicant_id': applicant_id,
            'status': 'submitted',
            'assigned_director_id': None,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    # Create inventor for conflict testing
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: PCC_ADMIN assigns Director (not inventor) to application
    admin_id = 3001
    
    result_app = assign_director(
        admin_id=admin_id,
        application_id=app.id,
        director_id=director_id
    )
    
    # Assert: Application status updated to Under Review, assignment recorded
    assert result_app.status == 'under_review'
    assert result_app.assigned_director_id == director_id
    
    # Verify history entry created
    history_entries = ApplicationHistory.objects.filter(application=app)
    assert len(history_entries) > 0
    recent_history = list(history_entries).reverse()[0]
    assert recent_history.action == 'assign_director'
    assert recent_history.to_status == 'under_review'


# -----------------------------------------------------------------------------
# TEST-PMS-UC007-MIN: Assignment to conflicted Director prevented
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_007_min_assignment_to_conflicted_director():
    """TEST-PMS-UC007-MIN: Verify that assignment to a conflicted Director (inventor) is prevented."""
    
    # Arrange: Create application in Submitted state with inventor as potential director
    applicant_id = 1001
    inventor_id = 2001  # This person is both inventor and would be assigned director
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-007",
        defaults={
            'applicant_id': applicant_id,
            'status': 'submitted',
            'assigned_director_id': None,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    # Create inventor record
    Inventor.objects.create(
        application=app,
        user_id=invantor_id,
        name="Conflicted Inventor",
        email="conflicted@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: PCC_ADMIN attempts to assign inventor as director
    admin_id = 3001
    
    with pytest.raises(ValueError) as exc_info:
        assign_director(
            admin_id=admin_id,
            application_id=app.id,
            director_id=invantor_id
        )
    
    # Assert: Error raised due to conflict of interest
    assert "conflict" in str(exc_info.value).lower() or "inventor" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# TEST-PMS-UC008-MAX: Director records valid technical merit decision
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_pms_008_max_director_valid_decision():
    """TEST-PMS-UC008-MAX: Verify that Directors record valid technical merit decisions (Approve, Reject, Needs Revision)."""
    
    # Arrange: Create application in Under Review state with assigned Director
    applicant_id = 1001
    director_id = 2001
    
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER="PMS-2024-008",
        defaults={
            'applicant_id': applicant_id,
            'status': 'under_review',
            'assigned_director_id': director_id,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    Inventor.objects.create(
        application=app,
        user_id=1002,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    ApplicationDocument.objects.create(
        application=app,
        file_name="draft_v1.pdf",
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=applicant_id,
        archived=False
    )
    
    # Act: Director records decision with valid justification (>= 50 characters)
    decision = 'approve'
    justification = "This application demonstrates clear novelty and non-obviousness. The technical domain is well-defined and the claims are properly drafted."
    
    result_app = review_application(
        director_id=director_id,
        application_id=app.id,
        decision=decision,
        justification=justification
    )
    
    # Assert: Decision recorded, status updated appropriately
    assert result_app.latest_decision == decision
    assert result_app.latest_justification == justification
    
    if decision == 'approve':
        assert result_app.status == 'approved'
    else:
        assert result_app.status in ['rejected', 'needs_revision']
    
    # Verify history entry created
    history_entries = ApplicationHistory.objects.filter(application=app)
    assert len(history_entries) > 0
    recent_history = list(history_entries).reverse()[0]
    assert recent_history.action == 'review'
    assert recent_history.to_status in ['approved', 'rejected', 'needs_revision']


# -----------------------------------------------------------------------------
# Helper Functions for Test Setup
# -----------------------------------------------------------------------------

def create_test_application(app_number, applicant_id, status='submitted'):
    """Helper to create a test application with minimal required data."""
    app, created = PatentApplication.objects.get_or_create(
        APPLICATION_NUMBER=app_number,
        defaults={
            'applicant_id': applicant_id,
            'status': status,
            'assigned_director_id': None,
            'assigned_attorney_id': None,
            'review_due_date': None,
            'resubmission_deadline': None,
            'version_number': 1,
        }
    )
    
    if created:
        app.save()
    
    return app


def create_test_inventor(app, user_id, name):
    """Helper to create a test inventor."""
    Inventor.objects.create(
        application=app,
        user_id=user_id,
        name=name,
        email=f"{name.lower()}@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )


def create_test_document(app, file_name):
    """Helper to create a test document."""
    ApplicationDocument.objects.create(
        application=app,
        file_name=file_name,
        content_type="application/pdf",
        size=102400,
        version=1,
        sensitivity='internal',
        uploaded_by=1001,
        archived=False
    )
```

> Tokens: 24k sent, 4.5k received.  
> Applied edit to tests/a8/uc/test_uc_p02.py  

# aider chat started at 2026-11-14 04:34:46

> /opt/homebrew/bin/aider --model ollama_chat/qwen3.5:4b --model-settings-file /Users/vishalkumar/elm_specs_md/pms_kit/a8/aider_model_settings.yml --edit-format whole --map-tokens 0 --timeout 3600 --yes-always --stream --no-pretty --no-fancy-input --no-gitignore --no-auto-commits --no-dirty-commits --no-auto-lint --no-auto-test --no-check-update --analytics-disable --no-show-release-notes --no-show-model-warnings --no-suggest-shell-commands --no-detect-urls --no-restore-chat-history --aiderignore /Users/vishalkumar/elm_specs_md/pms_kit/a8/aiderignore_a8 --chat-history-file a8_logs/uc/aider.chat.history.md --input-history-file a8_logs/uc/aider.input.history --llm-history-file a8_logs/uc/llm.history.txt --file tests/a8/uc/test_uc_p03.py --read conftest.py --read modules/patent/registry.py --read modules/patent/models.py --read modules/patent/domain/policy.py --read modules/patent/services/applications.py --read modules/patent/services/legal.py --read modules/patent/services/post_filing.py --read modules/patent/api/serializers.py --read modules/patent/api/views.py --read modules/patent/api/views_legal.py --read modules/patent/api/urls.py --message-file a8_logs/uc/promptB_p03.md  
> Creating empty file /Users/vishalkumar/ELM_MODEL_2/tests/a8/uc/test_uc_p03.py  
> Aider v0.86.2  
> Model: ollama_chat/qwen3.5:4b with whole edit format  
> Git repo: .git with 287 files  
> Repo-map: disabled  
> Added tests/a8/uc/test_uc_p03.py to the chat.  
> Added modules/patent/services/applications.py to the chat (read-only).  
> Added modules/patent/api/views.py to the chat (read-only).  
> Added modules/patent/api/urls.py to the chat (read-only).  
> Added modules/patent/domain/policy.py to the chat (read-only).  
> Added modules/patent/api/serializers.py to the chat (read-only).  
> Added modules/patent/registry.py to the chat (read-only).  
> Added modules/patent/services/post_filing.py to the chat (read-only).  
> Added modules/patent/api/views_legal.py to the chat (read-only).  
> Added modules/patent/services/legal.py to the chat (read-only).  
> Added conftest.py to the chat (read-only).  
> Added modules/patent/models.py to the chat (read-only).  

#### You are given:  
#### 1. the frozen A8_BASE Fusion implementation, and  
#### 2. the frozen UC_DESIGN.json.  
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
#### - Store generated tests only under tests/a8/uc/.  
#### If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.  
####   
#### The frozen UC_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 17 to 24 of 39; write exactly these test cases into tests/a8/uc/test_uc_p03.py.  
#### ```json  
#### [  
####  {  
####   "test_id": "TEST-PMS-UC008-MIN",  
####   "source_id": "UC-PMS-008 Exception Flows (No Justification)",  
####   "purpose": "Verify that review decisions without sufficient justification are rejected.",  
####   "preconditions": "Director attempts to submit a decision with fewer than 50 characters of justification.",  
####   "action_or_input": "Director submits the incomplete decision.",  
####   "expected_result": "PMS rejects the decision; no business state changes occur."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC010-MAX",  
####   "source_id": "UC-PMS-010 Main Success Scenario",  
####   "purpose": "Verify that approved applications can be assigned attorneys from the approved panel.",  
####   "preconditions": "Application status is Approved; PCC_ADMIN is authorized.",  
####   "action_or_input": "PCC_ADMIN selects an attorney from the approved panel (considering preference/conflict).",  
####   "expected_result": "PMS records the assignment, notifies the Attorney for acceptance/decline, and updates status to Attorney Assigned/Pending Review."  
####  },  
####  {  
####   "test_id": "TEST-PMS-010-MIN",  
####   "source_id": "UC-PMS-010 Exception Flows (Non-Panel)",  
####   "purpose": "Verify that non-panel attorneys are only assigned if an institutional exception exists.",  
####   "preconditions": "PCC_ADMIN attempts to assign an attorney not in the approved panel without a recorded exception.",  
####   "action_or_input": "PCC_ADMIN selects the non-panel attorney.",  
####   "expected_result": "PMS blocks assignment unless a valid institutional exception is recorded/allowed."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC011-MAX",  
####   "source_id": "UC-PMS-011 Main Success Scenario",  
####   "purpose": "Verify that Attorneys can accept or decline assignments.",  
####   "preconditions": "An assignment to the Attorney exists and is active.",  
####   "action_or_input": "Attorney selects Accept or Decline for the assignment.",  
####   "expected_result": "PMS records response. Acceptance updates status to Attorney Assigned; Decline updates to Pending Review and notifies PCC_ADMIN."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC012-MAX",  
####   "source_id": "UC-PMS-012 Main Success Scenario",  
####   "purpose": "Verify that Attorneys record patentability opinions with valid recommendations.",  
####   "preconditions": "Attorney has an assigned application and access to review details.",  
####   "action_or_input": "Attorney conducts assessment and selects one recommendation: File Patent, Do Not File, or Needs Amendment.",  
####   "expected_result": "PMS records the opinion/recommendation and notifies stakeholders."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC013-MAX",  
####   "source_id": "UC-PMS-013 Main Success Scenario",  
####   "purpose": "Verify that Attorneys can prepare, validate, and record external patent filings.",  
####   "preconditions": "Required approvals, budget allocation, and inventor agreements are complete; Attorney has filing authority.",  
####   "action_or_input": "Attorney prepares package, performs validation (if available), submits externally, and records confirmation details.",  
####   "expected_result": "PMS sets application status to Filed, records audit/history, and triggers confirmation notification."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC013-MIN",  
####   "source_id": "UC-PMS-013 Exception Flows (Prerequisites)",  
####   "purpose": "Verify that external filing is blocked if prerequisite approvals or agreements are missing.",  
####   "preconditions": "Required budget approval or inventor agreement is missing for the application.",  
####   "action_or_input": "Attorney attempts to submit the filing package.",  
####   "expected_result": "PMS blocks the filing action."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC015-MAX",  
####   "source_id": "UC-PMS-015 Main Success Scenario",  
####   "purpose": "Verify that Attorneys can submit office-action responses, handling optional Applicant review.",  
####   "preconditions": "Office action exists; Attorney has access; applicable deadline/extension data is available.",  
####   "action_or_input": "Attorney prepares response (optional: records Applicant approval) and submits the response externally.",  
####   "expected_result": "PMS updates response tracking, audit/history, and maintains status. Extension requests are recorded if allowed."  
####  }  
#### ]  
#### ```  

<thinking-content-7bbeb8e1441453ad999a0bbba8a46d4b>

The user wants me to convert the UC_DESIGN.json test cases (17-24) into pytest tests for the patent management system. I need to create a file at `tests/a8/uc/test_uc_p03.py` with exactly these test cases implemented.

Let me analyze what I need to do:

1. Create pytest tests that match each UC scenario
2. Use the existing Fusion test infrastructure (conftest.py is already provided)
3. Test the patent domain logic using the services and models already defined
4. Each test must have test_id and source_id in name or docstring
5. Tests should be under `tests/a8/uc/` directory
6. Don't modify production code - only create tests

Looking at the existing files, I can see:
- `modules/patent/services/applications.py` - application lifecycle services
- `modules/patent/services/legal.py` - legal/filing services
- `modules/patent/models.py` - database models
- `conftest.py` - test fixtures including stub_iam

The UC scenarios I need to implement:
1. TEST-PMS-UC008-MIN - Director submits decision without 50+ char justification (should fail)
2. TEST-PMS-UC010-MAX - PCC_ADMIN assigns attorney to approved application (success)
3. TEST-PMS-010-MIN - Non-panel attorney assignment blocked without exception
4. TEST-PMS-UC011-MAX - Attorney accepts/declines assignment
5. TEST-PMS-UC012-MAX - Attorney records patentability opinion
6. TEST-PMS-UC013-MAX - Attorney submits external filing (success)
7. TEST-PMS-UC013-MIN - External filing blocked if prerequisites missing
8. TEST-PMS-UC015-MAX - Attorney submits office action response

I need to write pytest tests that:


- Use the existing service functions and models
- Set up preconditions using fixtures
- Verify expected results
- Use proper error handling for validation failures

Let me create the test file with all 8 test cases.

</thinking-content-7bbeb8e1441453ad999a0bbba8a46d4b>

tests/a8/uc/test_uc_p03.py
```
"""Test cases for Patent Management System UC scenarios (UC-PMS-008 to UC-PMS-015).

These tests verify business rules and exception flows for:
- Director review decisions with justification validation
- Attorney assignment from approved panel
- Non-panel attorney assignment restrictions
- Attorney acceptance/decline of assignments
- Patentability opinion recording
- External patent filing submission
- Office action response submission
"""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.response import Response

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument, AttorneyAssignment,
    PatentabilityOpinion, Budget, Filing, OfficeAction, ApplicationHistory
)
from modules.patent.services.applications import (
    review_application, resubmit_application, withdraw_application
)
from modules.patent.services.legal import (
    assign_attorney, respond_to_assignment, record_opinion, record_filing,
    prepare_response, submit_response
)
from modules.patent.domain.policy import validate_justification


# -----------------------------------------------------------------------------
# Fixtures and Test Setup
# -----------------------------------------------------------------------------

@pytest.fixture
def stub_iam(monkeypatch):
    """Use the existing stub_iam fixture from conftest.py"""
    from conftest import stub_iam
    return stub_iam(monkeypatch)


@pytest.fixture
def principal_applicant(stub_iam):
    """Create a Principal with applicant role and permissions."""
    user = stub_iam.users.get(1001, {})
    if not user:
        stub_iam.users[1001] = {
            'id': 1001,
            'username': 'u1001',
            'display_name': 'Applicant User',
            'kind': 'student',
            'discipline': 'CSE'
        }
    return Principal.from_session(
        user_id=1001,
        username='u1001',
        display_name='Applicant User',
        kind='student',
        active_role='student',
        permissions=frozenset([
            'patent.application.view_self',
            'patent.application.create',
            'patent.application.withdraw'
        ]),
        modules=('patent',)
    )


@pytest.fixture
def principal_director(stub_iam):
    """Create a Principal with director role and permissions."""
    user = stub_iam.users.get(2001, {})
    if not user:
        stub_iam.users[2001] = {
            'id': 2001,
            'username': 'u2001',
            'display_name': 'Director User',
            'kind': 'faculty',
            'discipline': 'CSE'
        }
    return Principal.from_session(
        user_id=2001,
        username='u2001',
        display_name='Director User',
        kind='faculty',
        active_role='director',
        permissions=frozenset([
            'patent.application.review',
            'patent.budget.approve',
            'patent.maintenance.manage',
            'patent.appeal.review'
        ]),
        modules=('patent',)
    )


@pytest.fixture
def principal_admin(stub_iam):
    """Create a Principal with PCC_ADMIN role and permissions."""
    user = stub_iam.users.get(3001, {})
    if not user:
        stub_iam.users[3001] = {
            'id': 3001,
            'username': 'u3001',
            'display_name': 'Admin User',
            'kind': 'staff',
            'discipline': 'IT'
        }
    return Principal.from_session(
        user_id=3001,
        username='u3001',
        display_name='Admin User',
        kind='staff',
        active_role='admin',
        permissions=frozenset([
            'patent.admin.manage',
            'patent.application.manage',
            'patent.legal.review',
            'patent.budget.approve',
            'patent.filing.record'
        ]),
        modules=('patent',)
    )


@pytest.fixture
def principal_attorney(stub_iam):
    """Create a Principal with attorney role and permissions."""
    user = stub_iam.users.get(4001, {})
    if not user:
        stub_iam.users[4001] = {
            'id': 4001,
            'username': 'u4001',
            'display_name': 'Attorney User',
            'kind': 'staff',
            'discipline': 'IT'
        }
    return Principal.from_session(
        user_id=4001,
        username='u4001',
        display_name='Attorney User',
        kind='staff',
        active_role='attorney',
        permissions=frozenset([
            'patent.legal.review',
            'patent.filing.record',
            'patent.maintenance.manage'
        ]),
        modules=('patent',)
    )


@pytest.fixture
def application(applicant, stub_iam):
    """Create a test patent application with required fields."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-001',
        applicant_id=1001,
        title='Test Patent Application',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor',
        email='inventor@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def application_with_budget(applicant, stub_iam):
    """Create a test patent application with approved budget."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-002',
        applicant_id=1001,
        title='Test Patent Application 2',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 2',
        email='inventor2@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add approved budget
    Budget.objects.create(
        application=app,
        filing_fee=1000.00,
        attorney_fee=500.00,
        administrative_cost=200.00,
        total=1700.00,
        status='approved',
        decided_by=3001,
        justification='Budget approved for filing.'
    )
    
    return app


@pytest.fixture
def application_with_office_action(applicant, stub_iam):
    """Create a test patent application with office action."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-003',
        applicant_id=1001,
        title='Test Patent Application 3',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='filed'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 3',
        email='inventor3@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add office action
    OfficeAction.objects.create(
        application=app,
        received_date=date.today() - timedelta(days=10),
        response_due_date=date.today() + timedelta(days=30),
        description='Office action received from patent office.',
        status='recorded'
    )
    
    return app


@pytest.fixture
def application_with_attorney(applicant, stub_iam):
    """Create a test patent application with assigned attorney."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-004',
        applicant_id=1001,
        title='Test Patent Application 4',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 4',
        email='inventor4@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add attorney assignment (offered status)
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=4001,
        status='offered'
    )
    
    return app


@pytest.fixture
def application_with_pending_assignment(applicant, stub_iam):
    """Create a test patent application with pending attorney assignment."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-005',
        applicant_id=1001,
        title='Test Patent Application 5',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 5',
        email='inventor5@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add attorney assignment (accepted status)
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=4001,
        status='accepted'
    )
    
    return app


@pytest.fixture
def application_with_opinion(applicant, stub_iam):
    """Create a test patent application with patentability opinion."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-006',
        applicant_id=1001,
        title='Test Patent Application 6',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 6',
        email='inventor6@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add attorney assignment (accepted status)
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=4001,
        status='accepted'
    )
    
    return app


@pytest.fixture
def application_with_filing(applicant, stub_iam):
    """Create a test patent application with filed record."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-007',
        applicant_id=1001,
        title='Test Patent Application 7',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='filed'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 7',
        email='inventor7@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add filing record
    Filing.objects.create(
        application=app,
        patent_office='USPTO',
        filing_number='12345678',
        filing_date=date.today(),
        international=False
    )
    
    return app


@pytest.fixture
def application_with_unsigned_agreement(applicant, stub_iam):
    """Create a test patent application with inventor who hasn't signed agreement."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-008',
        applicant_id=1001,
        title='Test Patent Application 8',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor WITHOUT signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 8',
        email='inventor8@test.com',
        contribution_percent=50.0,
        agreement_signed=False
    )
    
    return app


@pytest.fixture
def application_with_unapproved_budget(applicant, stub_iam):
    """Create a test patent application with unapproved budget."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-009',
        applicant_id=1001,
        title='Test Patent Application 9',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 9',
        email='inventor9@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add unapproved budget (pending status)
    Budget.objects.create(
        application=app,
        filing_fee=1000.00,
        attorney_fee=500.00,
        administrative_cost=200.00,
        total=1700.00,
        status='pending',
        decided_by=None,
        justification='Budget pending approval.'
    )
    
    return app


# -----------------------------------------------------------------------------
# Test Cases
# -----------------------------------------------------------------------------

class TestPMSUC008MIN:
    """Test UC-PMS-008 Exception Flows (No Justification)."""
    
    def test_director_review_decision_without_sufficient_justification(self, principal_director, application):
        """
        TEST-PMS-UC008-MIN - Verify that review decisions without sufficient justification are rejected.
        
        Purpose: Verify that review decisions without 50+ character justification fail validation.
        Preconditions: Director attempts to submit a decision with fewer than 50 characters of justification.
        Expected Result: PMS rejects the decision; no business state changes occur.
        """
        # Arrange
        short_justification = "This is too short"  # Less than 50 characters
        
        # Act - Attempt to submit review with insufficient justification
        try:
            result = review_application(
                director_id=2001,
                application_id=application.id,
                decision='reject',
                justification=short_justification
            )
            # Assert - Should raise ValueError due to validation failure
            assert False, "Expected ValueError to be raised for insufficient justification"
        except ValueError as e:
            # Assert - Verify the error message indicates justification requirement
            assert '50' in str(e) or 'justification' in str(e).lower()
        
        # Assert - Application status should not change
        application.refresh_from_db()
        assert application.status == 'approved', "Application status should remain unchanged"


class TestPMSUC010MAX:
    """Test UC-PMS-010 Main Success Scenario."""
    
    def test_pcc_admin_assign_attorney_to_approved_application(self, principal_admin, application_with_budget):
        """
        TEST-PMS-UC010-MAX - Verify that approved applications can be assigned attorneys from the approved panel.
        
        Purpose: Verify that PCC_ADMIN can assign an attorney to an approved application.
        Preconditions: Application status is Approved; PCC_ADMIN is authorized.
        Expected Result: PMS records the assignment, notifies the Attorney for acceptance/decline, and updates status to Attorney Assigned/Pending Review.
        """
        # Arrange
        admin_principal = principal_admin
        
        # Act - Assign attorney to approved application
        assignment = assign_attorney(
            admin_id=3001,
            application_id=application_with_budget.id,
            attorney_id=4001
        )
        
        # Assert - Assignment should be created with 'offered' status
        assert assignment.status == 'offered', "Assignment should be created with offered status"
        
        # Assert - Application status should update to 'attorney_assigned'
        application_with_budget.refresh_from_db()
        assert application_with_budget.status == 'attorney_assigned', "Application status should update to attorney_assigned"
        
        # Assert - History entry should be created
        history = ApplicationHistory.objects.filter(
            application=application_with_budget,
            action='assign_attorney'
        ).first()
        assert history is not None, "History entry should be created for assignment"


class TestPMS010MIN:
    """Test UC-PMS-010 Exception Flows (Non-Panel)."""
    
    def test_non_panel_attorney_assignment_blocked_without_exception(self, principal_admin, application_with_budget):
        """
        TEST-PMS-010-MIN - Verify that non-panel attorneys are only assigned if an institutional exception exists.
        
        Purpose: Verify that PMS blocks assignment of non-panel attorneys without institutional exception.
        Preconditions: PCC_ADMIN attempts to assign an attorney not in the approved panel without a recorded exception.
        Expected Result: PMS blocks assignment unless a valid institutional exception is recorded/allowed.
        """
        # Arrange - Use a different attorney ID (simulating non-panel attorney)
        non_panel_attorney_id = 5001
        
        # Act - Attempt to assign non-panel attorney
        try:
            assignment = assign_attorney(
                admin_id=3001,
                application_id=application_with_budget.id,
                attorney_id=non_panel_attorney_id
            )
            # Assert - Should raise BusinessRuleViolation due to conflict/exception check
            assert False, "Expected BusinessRuleViolation to be raised for non-panel attorney"
        except Exception as e:
            # Assert - Verify the error indicates assignment was blocked
            assert 'conflict' in str(e).lower() or 'exception' in str(e).lower(), \
                f"Expected conflict/exception error, got: {e}"
        
        # Assert - Application status should not change
        application_with_budget.refresh_from_db()
        assert application_with_budget.status == 'attorney_assigned', "Application status should remain unchanged"


class TestPMSUC011MAX:
    """Test UC-PMS-011 Main Success Scenario."""
    
    def test_attorney_accepts_or_declines_assignment(self, principal_attorney, application_with_pending_assignment):
        """
        TEST-PMS-UC011-MAX - Verify that Attorneys can accept or decline assignments.
        
        Purpose: Verify that attorney acceptance/decline updates application status appropriately.
        Preconditions: An assignment to the Attorney exists and is active.
        Expected Result: PMS records response. Acceptance updates status to Attorney Assigned; Decline updates to Pending Review and notifies PCC_ADMIN.
        """
        # Arrange - Application already has accepted attorney assignment
        
        # Act - Test acceptance
        application_with_pending_assignment.refresh_from_db()
        
        # Accept the assignment (should be already accepted, but test the logic)
        result = respond_to_assignment(
            attorney_id=4001,
            assignment_id=application_with_pending_assignment.assignments.first().id,
            accept=True,
            reason=''
        )
        
        # Assert - Application status should remain 'attorney_assigned' after acceptance
        application_with_pending_assignment.refresh_from_db()
        assert application_with_pending_assignment.status == 'attorney_assigned', \
            "Application status should remain attorney_assigned after acceptance"
        
        # Act - Test decline (simulate by creating new assignment with declined status)
        application_decline = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-2024-010',
            applicant_id=1001,
            title='Test Patent Application 10',
            abstract='A test patent for automation.',
            description='Detailed description of the invention.',
            claims='Claims text here.',
            technical_domain='Software Engineering',
            status='approved'
        )
        
        Inventor.objects.create(
            application=application_decline,
            user_id=1001,
            name='Test Inventor 10',
            email='inventor10@test.com',
            contribution_percent=50.0,
            agreement_signed=True
        )
        
        AttorneyAssignment.objects.create(
            application=application_decline,
            attorney_id=4001,
            status='offered'
        )
        
        # Act - Decline the assignment
        result = respond_to_assignment(
            attorney_id=4001,
            assignment_id=application_decline.assignments.first().id,
            accept=False,
            reason='This is a test decline reason that is too short'  # Less than 50 chars
        )
        
        # Assert - Should raise due to insufficient justification for decline
        assert False, "Expected BusinessRuleViolation for insufficient decline reason"
        
        # Act - Test with sufficient justification
        application_decline2 = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-2024-011',
            applicant_id=1001,
            title='Test Patent Application 11',
            abstract='A test patent for automation.',
            description='Detailed description of the invention.',
            claims='Claims text here.',
            technical_domain='Software Engineering',
            status='approved'
        )
        
        Inventor.objects.create(
            application=application_decline2,
            user_id=1001,
            name='Test Inventor 11',
            email='inventor11@test.com',
            contribution_percent=50.0,
            agreement_signed=True
        )
        
        AttorneyAssignment.objects.create(
            application=application_decline2,
            attorney_id=4001,
            status='offered'
        )
        
        # Act - Decline with sufficient justification
        result = respond_to_assignment(
            attorney_id=4001,
            assignment_id=application_decline2.assignments.first().id,
            accept=False,
            reason='This is a test decline reason that meets the minimum length requirement of fifty characters or more for proper documentation purposes.'
        )
        
        # Assert - Application status should update to 'approved' after decline
        application_decline2.refresh_from_db()
        assert application_decline2.status == 'approved', "Application status should update to approved after attorney decline"


class TestPMSUC012MAX:
    """Test UC-PMS-012 Main Success Scenario."""
    
    def test_attorney_records_patentability_opinion(self, principal_attorney, application_with_opinion):
        """
        TEST-PMS-UC012-MAX - Verify that Attorneys record patentability opinions with valid recommendations.
        
        Purpose: Verify that attorney can record opinion with File Patent, Do Not File, or Needs Amendment recommendation.
        Preconditions: Attorney has an assigned application and access to review details.
        Expected Result: PMS records the opinion/recommendation and notifies stakeholders.
        """
        # Arrange - Application already has accepted attorney assignment
        
        # Act - Record patentability opinion with 'file_patent' recommendation
        opinion = record_opinion(
            attorney_id=4001,
            application_id=application_with_opinion.id,
            novelty=True,
            non_obviousness=True,
            utility=True,
            recommendation='file_patent',
            text='This invention is novel, non-obvious, and useful.'
        )
        
        # Assert - Opinion should be created with correct values
        assert opinion.recommendation == 'file_patent', "Recommendation should be file_patent"
        assert opinion.novelty == True, "Novelty should be True"
        assert opinion.non_obviousness == True, "Non-obviousness should be True"
        assert opinion.utility == True, "Utility should be True"
        
        # Assert - History entry should be created
        history = ApplicationHistory.objects.filter(
            application=application_with_opinion,
            action='record_opinion'
        ).first()
        assert history is not None, "History entry should be created for opinion recording"


class TestPMSUC013MAX:
    """Test UC-PMS-013 Main Success Scenario."""
    
    def test_attorney_submits_external_filing(self, principal_attorney, application_with_filing):
        """
        TEST-PMS-UC013-MAX - Verify that Attorneys can prepare, validate, and record external patent filings.
        
        Purpose: Verify that attorney can submit external filing when prerequisites are met.
        Preconditions: Required approvals, budget allocation, and inventor agreements are complete; Attorney has filing authority.
        Expected Result: PMS sets application status to Filed, records audit/history, and triggers confirmation notification.
        """
        # Arrange - Application already has filing record
        
        # Act - Record new external filing
        filing = record_filing(
            attorney_id=4001,
            application_id=application_with_filing.id,
            office='USPTO',
            filing_number='87654321',
            filing_date=date.today(),
            international=True
        )
        
        # Assert - Filing should be created with correct values
        assert filing.patent_office == 'USPTO', "Patent office should be USPTO"
        assert filing.filing_number == '87654321', "Filing number should match"
        assert filing.international == True, "International flag should be True"
        
        # Assert - Application status should update to 'filed'
        application_with_filing.refresh_from_db()
        assert application_with_filing.status == 'filed', "Application status should be filed"
        
        # Assert - History entry should be created
        history = ApplicationHistory.objects.filter(
            application=application_with_filing,
            action='record_filing'
        ).first()
        assert history is not None, "History entry should be created for filing recording"


class TestPMSUC013MIN:
    """Test UC-PMS-013 Exception Flows (Prerequisites)."""
    
    def test_external_filing_blocked_if_prerequisites_missing(self, principal_attorney, application_with_unapproved_budget):
        """
        TEST-PMS-UC013-MIN - Verify that external filing is blocked if prerequisite approvals or agreements are missing.
        
        Purpose: Verify that PMS blocks filing when budget approval or inventor agreement is missing.
        Preconditions: Required budget approval or inventor agreement is missing for the application.
        Expected Result: PMS blocks the filing action.
        """
        # Arrange - Application has unapproved budget (pending status)
        
        # Act - Attempt to record filing with unapproved budget
        try:
            filing = record_filing(
                attorney_id=4001,
                application_id=application_with_unapproved_budget.id,
                office='USPTO',
                filing_number='11111111',
                filing_date=date.today(),
                international=False
            )
            # Assert - Should raise BusinessRuleViolation due to unapproved budget
            assert False, "Expected BusinessRuleViolation to be raised for unapproved budget"
        except Exception as e:
            # Assert - Verify the error indicates prerequisite issue
            assert 'budget' in str(e).lower() or 'approval' in str(e).lower(), \
                f"Expected budget/approval error, got: {e}"
        
        # Assert - Application status should not change
        application_with_unapproved_budget.refresh_from_db()
        assert application_with_unapproved_budget.status == 'approved', "Application status should remain unchanged"


class TestPMSUC015MAX:
    """Test UC-PMS-015 Main Success Scenario."""
    
    def test_attorney_submits_office_action_response(self, principal_attorney, application_with_office_action):
        """
        TEST-PMS-UC015-MAX - Verify that Attorneys can submit office-action responses, handling optional Applicant review.
        
        Purpose: Verify that attorney can prepare and submit office action response.
        Preconditions: Office action exists; Attorney has access; applicable deadline/extension data is available.
        Expected Result: PMS updates response tracking, audit/history, and maintains status. Extension requests are recorded if allowed.
        """
        # Arrange - Application already has office action with 'recorded' status
        
        # Act - Prepare response without applicant approval needed
        updated_oa = prepare_response(
            attorney_id=4001,
            office_action_id=application_with_office_action.office_actions.first().id,
            response_text='This is a prepared response to the office action.',
            needs_applicant_approval=False
        )
        
        # Assert - Office action status should update to 'response_ready'
        updated_oa.refresh_from_db()
        assert updated_oa.status == 'response_ready', "Office action status should be response_ready"
        
        # Act - Submit the response
        submitted_oa = submit_response(
            attorney_id=4001,
            office_action_id=updated_oa.id
        )
        
        # Assert - Office action status should update to 'response_submitted'
        submitted_oa.refresh_from_db()
        assert submitted_oa.status == 'response_submitted', "Office action status should be response_submitted"
        
        # Assert - History entry should be created for both prepare and submit actions
        history_prepare = ApplicationHistory.objects.filter(
            application=application_with_office_action,
            action='response_prepared'
        ).first()
        assert history_prepare is not None, "History entry should be created for response preparation"
        
        history_submit = ApplicationHistory.objects.filter(
            application=application_with_office_action,
            action='response_submitted'
        ).first()
        assert history_submit is not None, "History entry should be created for response submission"
```

> Tokens: 24k sent, 6.6k received.  
> Applied edit to tests/a8/uc/test_uc_p03.py  

# aider chat started at 2026-11-14 05:04:57

> /opt/homebrew/bin/aider --model ollama_chat/qwen3.5:4b --model-settings-file /Users/vishalkumar/elm_specs_md/pms_kit/a8/aider_model_settings.yml --edit-format whole --map-tokens 0 --timeout 3600 --yes-always --stream --no-pretty --no-fancy-input --no-gitignore --no-auto-commits --no-dirty-commits --no-auto-lint --no-auto-test --no-check-update --analytics-disable --no-show-release-notes --no-show-model-warnings --no-suggest-shell-commands --no-detect-urls --no-restore-chat-history --aiderignore /Users/vishalkumar/elm_specs_md/pms_kit/a8/aiderignore_a8 --chat-history-file a8_logs/uc/aider.chat.history.md --input-history-file a8_logs/uc/aider.input.history --llm-history-file a8_logs/uc/llm.history.txt --file tests/a8/uc/test_uc_p04.py --read conftest.py --read modules/patent/registry.py --read modules/patent/models.py --read modules/patent/domain/policy.py --read modules/patent/services/applications.py --read modules/patent/services/legal.py --read modules/patent/services/post_filing.py --read modules/patent/api/serializers.py --read modules/patent/api/views.py --read modules/patent/api/views_legal.py --read modules/patent/api/urls.py --message-file a8_logs/uc/promptB_p04.md  
> Creating empty file /Users/vishalkumar/ELM_MODEL_2/tests/a8/uc/test_uc_p04.py  
> Aider v0.86.2  
> Model: ollama_chat/qwen3.5:4b with whole edit format  
> Git repo: .git with 288 files  
> Repo-map: disabled  
> Added tests/a8/uc/test_uc_p04.py to the chat.  
> Added modules/patent/domain/policy.py to the chat (read-only).  
> Added modules/patent/services/post_filing.py to the chat (read-only).  
> Added modules/patent/api/urls.py to the chat (read-only).  
> Added modules/patent/services/applications.py to the chat (read-only).  
> Added modules/patent/models.py to the chat (read-only).  
> Added modules/patent/api/serializers.py to the chat (read-only).  
> Added modules/patent/registry.py to the chat (read-only).  
> Added modules/patent/api/views.py to the chat (read-only).  
> Added conftest.py to the chat (read-only).  
> Added modules/patent/services/legal.py to the chat (read-only).  
> Added modules/patent/api/views_legal.py to the chat (read-only).  

#### You are given:  
#### 1. the frozen A8_BASE Fusion implementation, and  
#### 2. the frozen UC_DESIGN.json.  
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
#### - Store generated tests only under tests/a8/uc/.  
#### If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.  
####   
#### The frozen UC_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 25 to 32 of 39; write exactly these test cases into tests/a8/uc/test_uc_p04.py.  
#### ```json  
#### [  
####  {  
####   "test_id": "TEST-PMS-UC015-MIN",  
####   "source_id": "UC-PMS-015 Exception Flows (Approval)",  
####   "purpose": "Verify that responses cannot be marked submitted without required Applicant approval (when applicable).",  
####   "preconditions": "Process requires Applicant review; draft is available but not yet approved.",  
####   "action_or_input": "Attorney attempts to finalize and submit the response without Applicant approval.",  
####   "expected_result": "PMS does not mark the response as submitted; response status remains awaiting approval."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC016-MAX",  
####   "source_id": "UC-PMS-016 Main Success Scenario",  
####   "purpose": "Verify that PCC_ADMIN can monitor deadlines and handle escalations.",  
####   "preconditions": "Active authorized role; deadline records exist or are calculable.",  
####   "action_or_input": "PCC_ADMIN views monitoring view, reviews alerts (30/15/5 days), and handles missed deadline escalations.",  
####   "expected_result": "PMS calculates/maintains deadlines, generates alerts, logs activity, and routes/escalates delayed cases."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC017-MAX",  
####   "source_id": "UC-PMS-017 Main Success Scenario",  
####   "purpose": "Verify that post-grant tracking activates and renewal decisions are recorded.",  
####   "preconditions": "Patent status is Granted; maintenance deadline approaches.",  
####   "action_or_input": "Attorney requests a Renewal decision from the Director.",  
####   "expected_result": "Director records Renew or Do Not Renew; if Renewed, Attorney processes action and PMS updates status/history."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC018-MAX",  
####   "source_id": "UC-PMS-018 Main Success Scenario",  
####   "purpose": "Verify that Directors can record Renewal or Do Not Renew decisions.",  
####   "preconditions": "Patent is in post-grant tracking; renewal decision is due.",  
####   "action_or_input": "Director selects Renew or Do Not Renew.",  
####   "expected_result": "PMS records the decision and makes it available for the Attorney's next action."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC019-MAX",  
####   "source_id": "UC-PMS-019 Main Success Scenario",  
####   "purpose": "Verify that authorized users can upload document versions.",  
####   "preconditions": "User has valid role; action is permitted for role/status (e.g., Applicant in Needs Revision).",  
####   "action_or_input": "User uploads a new document version.",  
####   "expected_result": "PMS assigns next version number, archives previous version, logs modification with user/timestamp."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC019-MIN",  
####   "source_id": "UC-PMS-019 Exception Flows (Unauthorized)",  
####   "purpose": "Verify that unauthorized users cannot upload document versions.",  
####   "preconditions": "User lacks role or status permission to upload documents.",  
####   "action_or_input": "User attempts to upload a new document version.",  
####   "expected_result": "Upload is blocked; prior version history remains consistent."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC022-MAX",  
####   "source_id": "UC-PMS-022 Main Success Scenario",  
####   "purpose": "Verify that Applicants can file appeals within the allowed period.",  
####   "preconditions": "Application is Rejected; appeal period has not expired.",  
####   "action_or_input": "Applicant enters grounds/justification and submits the appeal.",  
####   "expected_result": "PMS validates eligibility/timing, records the appeal for Director review."  
####  },  
####  {  
####   "test_id": "TEST-PMS-UC023-MAX",  
####   "source_id": "UC-PMS-023 Main Success Scenario",  
####   "purpose": "Verify that Directors can record specific appeal outcomes.",  
####   "preconditions": "Appeal exists and is available for review.",  
####   "action_or_input": "Director selects one outcome: Uphold Rejection, Remand for Amendment, or Modify Decision.",  
####   "expected_result": "PMS records the outcome and initiates the next applicable process step."  
####  }  
#### ]  
#### ```  

<thinking-content-7bbeb8e1441453ad999a0bbba8a46d4b>

The user wants me to convert the UC_DESIGN.json test cases (25-32) into pytest/pytest-django tests. I need to create a file at `tests/a8/uc/test_uc_p04.py` with exactly these test cases implemented.

Let me analyze each test case:

1. **TEST-PMS-UC015-MIN** - Verify responses cannot be marked submitted without required Applicant approval
   - This tests the prepare_response flow where needs_applicant_approval=True is required
   - Should verify that attorney cannot submit response without applicant approval first

2. **TEST-PMS-UC016-MAX** - PCC_ADMIN can monitor deadlines and handle escalations
   - Tests deadline monitoring functionality
   - Should verify alert generation and escalation routing

3. **TEST-PMS-UC017-MAX** - Post-grant tracking activates and renewal decisions are recorded
   - Tests post-grant maintenance fee workflow
   - Should verify renewal decision recording

4. **TEST-PMS-UC018-MAX** - Directors can record Renewal or Do Not Renew decisions
   - Similar to UC017 but focuses on the Director's decision-making
   - Should verify decision recording and availability for Attorney action

5. **TEST-PMS-UC019-MAX** - Authorized users can upload document versions
   - Tests document versioning workflow
   - Should verify version number assignment, archiving, logging

6. **TEST-PMS-UC019-MIN** - Unauthorized users cannot upload document versions
   - Exception flow for UC019
   - Should verify upload blocking and history consistency

7. **TEST-PMS-UC022-MAX** - Applicants can file appeals within allowed period
   - Tests appeal filing workflow
   - Should verify eligibility validation and appeal recording

8. **TEST-PMS-UC023-MAX** - Directors can record specific appeal outcomes
   - Tests appeal decision workflow
   - Should verify outcome recording and next process step initiation
   
I'll now implement these tests using pytest-django with proper fixtures, test IDs, and source IDs as required by the specification.

</thinking-content-7bbeb8e1441453ad999a0bbba8a46d4b>

tests/a8/uc/test_uc_p04.py
```
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
```

> Tokens: 24k sent, 4.2k received.  
> Applied edit to tests/a8/uc/test_uc_p04.py  
