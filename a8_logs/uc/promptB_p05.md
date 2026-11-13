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

The frozen UC_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 33 to 39 of 39; write exactly these test cases into tests/a8/uc/test_uc_p05.py.
```json
[
 {
  "test_id": "TEST-PMS-UC028-MAX",
  "source_id": "UC-PMS-028 Main Success Scenario",
  "purpose": "Verify that authorized actors can view audit/compliance logs.",
  "preconditions": "Authorized actor (PCC_ADMIN/Director); access to audit information.",
  "action_or_input": "Actor opens audit/compliance logs and selects scope (application/user/action).",
  "expected_result": "PMS displays available audit records with required fields; no business state changes."
 },
 {
  "test_id": "TEST-PMS-UC028-MIN",
  "source_id": "UC-PMS-028 Exception Flows",
  "purpose": "Verify that unauthorized audit access is blocked.",
  "preconditions": "Actor attempts to view audit logs without authorization.",
  "action_or_input": "Actor accesses the restricted audit record.",
  "expected_result": "PMS blocks access; no audit data is displayed or altered."
 },
 {
  "test_id": "TEST-PMS-UC029-MAX",
  "source_id": "UC-PMS-029 Main Success Scenario",
  "purpose": "Verify that Applicants can approve Office Action draft responses when required.",
  "preconditions": "Process requires Applicant review; a draft response exists.",
  "action_or_input": "Applicant reviews and records approval of the draft response.",
  "expected_result": "PMS records the approval, allowing the Attorney to finalize/submit."
 },
 {
  "test_id": "TEST-PMS-UC031-MAX",
  "source_id": "UC-PMS-031 Main Success Scenario",
  "purpose": "Verify that Directors can view authorized reports and analytics.",
  "preconditions": "Director has an authorized PMS role.",
  "action_or_input": "Director selects a report/analytics view (e.g., portfolio, workload).",
  "expected_result": "PMS generates output within Director's scope/domain and logs access."
 },
 {
  "test_id": "TEST-PMS-UC032-MAX",
  "source_id": "UC-PMS-032 Main Success Scenario",
  "purpose": "Verify that Directors can view workflow oversight information.",
  "preconditions": "Director has an authorized role and domain scope.",
  "action_or_input": "Director opens workflow oversight dashboard.",
  "expected_result": "PMS displays workflow states, pending actions, and oversight info within the Director's domain."
 },
 {
  "test_id": "TEST-PMS-UC033-MAX",
  "source_id": "UC-PMS-033 Main Success Scenario",
  "purpose": "Verify that Attorneys can record legal advice for applications.",
  "preconditions": "Attorney has a valid role and access to the application.",
  "action_or_input": "Attorney records legal advice/opinion information for an application.",
  "expected_result": "PMS associates the advice with the application history/audit record as applicable."
 },
 {
  "test_id": "TEST-PMS-UC033-MIN",
  "source_id": "UC-PMS-033 Exception Flows",
  "purpose": "Verify that unauthorized legal advice recording is blocked.",
  "preconditions": "Attorney attempts to record advice for an application they do not have access to.",
  "action_or_input": "Attorney selects the restricted application to record advice.",
  "expected_result": "Recording fails; no unrelated application state changes occur."
 }
]
```
