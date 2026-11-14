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

The frozen WF_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 9 to 14 of 14; write exactly these test cases into tests/a8/wf/test_wf_p02.py.
```json
[
 {
  "test_id": "T-009",
  "source_id": "BR-PMS-067; BR-PMS-068; BR-PMS-069; BR-PMS-070",
  "purpose": "Validate withdrawal eligibility checks and co-inventor consent collection when applicable before 'Before Filing' or 'Under Review' states.",
  "preconditions": "Application is in a configured pre-filing state (e.g., Submitted, Under Review); Withdrawal reason provided.",
  "action_or_input": "Applicant initiates UC-PMS-006 to Withdraw Patent Application.",
  "expected_result": "PMS validates if current state is withdrawal-eligible per configuration; collects co-inventor consent if required by process; updates status to 'Withdrawn' and removes from queue.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-010",
  "source_id": "UC-PMS-018",
  "purpose": "Validate Director's decision to Renew or Do Not Renew for maintenance fee cycles and transition logic.",
  "preconditions": "Application status is 'Granted' / Maintenance Cycle Active; Attorney has requested Renewal Decision from Director.",
  "action_or_input": "Director makes a 'Renew' or 'Do Not Renew' decision (UC-PMS-018).",
  "expected_result": "PMS records the decision outcome; if 'Renew', processes maintenance action, records transaction/status, and schedules next cycle. If 'Do Not Renew', records decision and ends current cycle.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-011",
  "source_id": "BR-PMS-048; BR-PMS-052; BR-PMS-053",
  "purpose": "Validate Budget Approval and Rejection logic including cost validation.",
  "preconditions": "Application is 'Approved'; Director reviews budget.",
  "action_or_input": "Director decides to Approve or Reject the budget (validating costs against threshold and availability where applicable).",
  "expected_result": "PMS updates status/budget records accordingly; if Rejected, ensures no downstream auto-approval occurs.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-012",
  "source_id": "BR-PMS-055; BR-PMS-056",
  "purpose": "Validate pre-filing readiness checks and successful external filing transition.",
  "preconditions": "Application is 'Approved'; All pre-filing prerequisites (budget, agreement, expert approval) are complete.",
  "action_or_input": "Attorney initiates UC-PMS-013 to Prepare and Record External Patent Filing.",
  "expected_result": "PMS verifies format compliance and prerequisites; updates status to 'Filed' and captures filing ID/date.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-013",
  "source_id": "BR-PMS-146; BR-PMS-065; BR-PMS-066",
  "purpose": "Validate Office Action response submission and deadline tracking logic.",
  "preconditions": "Application is 'Filed / Post-Filing Active'; Attorney has received an Office Action.",
  "action_or_input": "Attorney records, prepares, and submits a response within the applicable deadline or permitted extension period (UC-PMS-015).",
  "expected_result": "PMS updates status (e.g., to 'Response Submitted'), logs official communication history, and verifies adherence to time-bound rules.",
  "test_type": "Functional"
 },
 {
  "test_id": "T-014",
  "source_id": "BR-PMS-146; BR-PMS-065; BR-PMS-066",
  "purpose": "Validate conditional workflow branching where Applicant review is required for Office Action response.",
  "preconditions": "Application is 'Filed'; Office action received; System determines Applicant review is REQUIRED (e.g., per process rules).",
  "action_or_input": "Applicant reviews and approves the Attorney's draft response via UC-PMS-029.",
  "expected_result": "PMS transitions state from 'Awaiting Applicant Approval' to 'Response Submitted' upon approval, triggering notification of finalization.",
  "test_type": "Functional"
 }
]
```
