You are given:
1. the frozen A8_BASE Fusion implementation, and
2. the frozen WF_DESIGN.json.
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
- Store generated tests only under tests/a8/wf/.
If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.

The frozen WF_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 1 to 8 of 14; write exactly these test cases into tests/a8/wf/test_wf_p01.py.
```json
[
 {
  "test_id": "T-001",
  "source_id": "UC-PMS-001",
  "purpose": "Validate submission validation, document compliance, and application ID assignment upon a valid initial submission.",
  "preconditions": "System running; Application draft exists with required fields, PDF documents under 50MB, and completed inventor agreement.",
  "action_or_input": "Applicant submits the patent application via UC-PMS-001.",
  "expected_result": "PMS validates requirements, assigns unique Application ID, sets status to 'Submitted', records history, and notifies stakeholders.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-002",
  "source_id": "UC-PMS-007",
  "purpose": "Validate assignment logic including expertise matching, conflict-of-interest checks, and status transition to 'Under Review'.",
  "preconditions": "Application is in 'Submitted' state; Eligible Directors exist.",
  "action_or_input": "PCC_ADMIN assigns the application to a Director (explicit or automatic routing).",
  "expected_result": "PMS verifies assignment criteria, rejects invalid conflicts if applicable, and updates status to 'Under Review' with notifications.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-003",
  "source_id": "BR-PMS-029; BR-PMS-030; BR-PMS-031",
  "purpose": "Validate Director's review process, justification length enforcement, status transition on approval.",
  "preconditions": "Application is in 'Under Review' state with valid documentation.",
  "action_or_input": "Director reviews the application and provides a detailed justification of at least 50 characters; decides to Approve.",
  "expected_result": "PMS stores decision, validates justification length, updates status to 'Approved', and notifies relevant parties.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-004",
  "source_id": "BR-PMS-029; BR-PMS-030; BR-PMS-031; BR-PMS-033",
  "purpose": "Validate revision submission loop where applicant addresses feedback within the 60-day resubmission period.",
  "preconditions": "Application status is 'Needs Revision' or 'Rejected' with valid Director justification logged.",
  "action_or_input": "Applicant resubmits application addressing Director's feedback within the applicable 60-day window via UC-PMS-005.",
  "expected_result": "PMS validates deadline compliance and content alignment, assigns new Application ID/Version control cycle, updates status to 'Submitted' or re-routes to assignment.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-005",
  "source_id": "BR-PMS-038",
  "purpose": "Validate automatic status transition to 'Expired' when resubmission deadline expires (system-enforced behavior).",
  "preconditions": "Application is in 'Needs Revision' state; Applicant has failed to resubmit within the applicable 60-day period.",
  "action_or_input": "System checks the current date against the rejection/revision decision date and applies rule BR-PMS-038.",
  "expected_result": "PMS automatically updates the application status to 'Expired' without actor intervention.",
  "test_type": "System"
 },
 {
  "test_id": "T-006",
  "source_id": "UC-PMS-022",
  "purpose": "Validate appeal submission rules, grounds justification recording, and transition to 'Appeal Submitted'.",
  "preconditions": "Application status is 'Rejected' with valid Director justification.",
  "action_or_input": "Applicant initiates the File Appeal Against Rejection process (UC-PMS-022) within the allowed time period.",
  "expected_result": "PMS validates appeal deadline, records grounds/justification, updates status to 'Appeal Submitted', and notifies Director.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-007",
  "source_id": "BR-PMS-095",
  "purpose": "Validate Director's ability to modify a rejected application decision during an appeal review.",
  "preconditions": "Application is in 'Appeal Submitted' state after being Rejected.",
  "action_or_input": "Director reviews the appeal and decides to 'Modify Decision'.",
  "expected_result": "PMS records the modification outcome, initiates next applicable process step (e.g., resubmission or new review cycle), and updates status accordingly.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-008",
  "source_id": "UC-PMS-027",
  "purpose": "Validate escalation handling and PCC_ADMIN monitoring for budget cases exceeding threshold limits.",
  "preconditions": "Application is 'Approved'; Budget review decision outcome is 'Escalated' (cost > threshold).",
  "action_or_input": "Director routes/escalates the case (simulating BR-PMS-051 outcome).",
  "expected_result": "PCC_ADMIN monitors and tracks the exceptional case, maintains status as 'Escalation Tracked / External Decision Pending' within PMS scope.",
  "test_type": "Functional"
 }
]
```
