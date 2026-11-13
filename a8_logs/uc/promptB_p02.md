You are given:
1. the frozen A8_BASE Fusion implementation, and
2. the frozen UC_DESIGN.json.
Convert these test designs into executable automated backend tests using pytest/pytest-django.
Rules:
- Implement exactly the supplied test cases.
- Do not add, remove, merge or reinterpret test cases.
- Preserve each specified expected result.
- Do not modify production code.
- Use the Django isolated test database.
- Reuse existing Fusion test infrastructure where appropriate.
- Do not mock the behavior being tested; mocks may be used only for unavailable external dependencies.
- Do not use xfail to hide failures.
- Every test must contain its test_id and source_id in its name or docstring.
- Store generated tests only under tests/a8/uc/.
If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.

The frozen UC_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 9 to 16 of 39; write exactly these test cases into tests/a8/uc/test_uc_p02.py.
```json
[
 {
  "test_id": "TEST-PMS-UC005-MAX",
  "source_id": "UC-PMS-005 Main Success Scenario",
  "purpose": "Verify that Applicants can revise applications within the feedback period.",
  "preconditions": "Application status is Needs Revision or Rejected, and the 60-day resubmission period has not expired.",
  "action_or_input": "Applicant reviews Director feedback, edits content/documents, and resubmits.",
  "expected_result": "PMS validates that revision addresses feedback, records the revised version, starts a new review cycle."
 },
 {
  "test_id": "TEST-PMS-UC005-MIN",
  "source_id": "UC-PMS-005 Exception Flows (Late Deadline)",
  "purpose": "Verify that resubmissions outside the 60-day deadline are blocked.",
  "preconditions": "The application is in a revisionable state but the resubmission period has expired.",
  "action_or_input": "Applicant attempts to resubmit a late revision.",
  "expected_result": "PMS changes application status to Expired and rejects the submission."
 },
 {
  "test_id": "TEST-PMS-UC005-MIN2",
  "source_id": "UC-PMS-005 Exception Flows (Ignoring Feedback)",
  "purpose": "Verify that resubmissions not addressing Director feedback are rejected.",
  "preconditions": "Application is in Needs Revision state; revision content does not address the recorded Director feedback.",
  "action_or_input": "Applicant attempts to submit a revision ignoring feedback points.",
  "expected_result": "PMS rejects the resubmission and retains the prior valid application state."
 },
 {
  "test_id": "TEST-PMS-UC006-MAX",
  "source_id": "UC-PMS-006 Main Success Scenario",
  "purpose": "Verify that Applicants can withdraw eligible pre-filing applications.",
  "preconditions": "Application status is withdrawal-eligible (pre-filing), and withdrawal is allowed per BR-PMS-068.",
  "action_or_input": "Applicant provides a withdrawal reason, confirms co-inventor consent if required, and confirms withdrawal.",
  "expected_result": "PMS sets status to Withdrawn, removes application from active queue, and records history/status change."
 },
 {
  "test_id": "TEST-PMS-UC006-MIN",
  "source_id": "UC-PMS-006 Exception Flows",
  "purpose": "Verify that withdrawal is blocked when application status is not withdrawal-eligible.",
  "preconditions": "Application has reached Filed status or is in a non-withdrawal-eligible state.",
  "action_or_input": "Applicant attempts to withdraw the application.",
  "expected_result": "PMS blocks withdrawal and retains the current valid state."
 },
 {
  "test_id": "TEST-PMS-UC007-MAX",
  "source_id": "UC-PMS-007 Main Success Scenario",
  "purpose": "Verify that Submitted applications are assigned to an eligible, non-conflicted Director.",
  "preconditions": "Application status is Submitted; PCC_ADMIN or automatic routing is active.",
  "action_or_input": "PCC_ADMIN selects a Director (not listed as inventor) to receive the application.",
  "expected_result": "PMS records assignment, sets status to Under Review, notifies Director, and initiates review timeline."
 },
 {
  "test_id": "TEST-PMS-UC007-MIN",
  "source_id": "UC-PMS-007 Exception Flows",
  "purpose": "Verify that assignment to a conflicted Director (inventor) is prevented.",
  "preconditions": "Application is Submitted; PCC_ADMIN attempts to assign to a Director listed as an inventor.",
  "action_or_input": "PCC_ADMIN selects the conflicted Director.",
  "expected_result": "PMS prevents assignment, leaves application status Submitted, and flags/raises the exceptional case."
 },
 {
  "test_id": "TEST-PMS-UC008-MAX",
  "source_id": "UC-PMS-008 Main Success Scenario",
  "purpose": "Verify that Directors record valid technical merit decisions (Approve, Reject, Needs Revision).",
  "preconditions": "Application is Under Review; Director is the assigned reviewer with no conflict.",
  "action_or_input": "Director selects a decision and enters justification of at least 50 characters.",
  "expected_result": "PMS records the decision/audit trail. Approved apps become eligible for attorney assignment; others trigger feedback to Applicant."
 }
]
```
