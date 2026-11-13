
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
