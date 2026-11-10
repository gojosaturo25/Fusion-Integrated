You are given:
1. the frozen A8_BASE Fusion implementation, and
2. the frozen FR_DESIGN.json.
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
- Store generated tests only under tests/a8/fr/.
If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 177 to 184 of 204; write exactly these test cases into tests/a8/fr/test_fr_p23.py.
```json
[
 {
  "test_id": "TEST-CFR-023-12",
  "source_id": "PMS-AFR-204",
  "purpose": "Verification of triggering notification for document version changes",
  "preconditions": "Version changed.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-13",
  "source_id": "PMS-AFR-206",
  "purpose": "Verification of limiting notification scope to system-generated emails (external infra outside)",
  "preconditions": "Notification trigger occurs.",
  "action_or_input": "Monitor external delivery logs vs PMS internal logs.",
  "expected_result": "PMS only triggers the event; actual delivery relies on external infrastructure."
 },
 {
  "test_id": "TEST-CFR-024-0",
  "source_id": "PMS-AFR-207",
  "purpose": "Verification of maintaining audit trail of PMS actions",
  "preconditions": "Action performed.",
  "action_or_input": "Access Audit Logs.",
  "expected_result": "Record exists in the log."
 },
 {
  "test_id": "TEST-CFR-024-1",
  "source_id": "PMS-AFR-208",
  "purpose": "Verification of logging all user actions",
  "preconditions": "User performs action.",
  "action_or_input": "Search Audit Logs for User ID.",
  "expected_result": "All logged actions are present."
 },
 {
  "test_id": "TEST-CFR-024-2",
  "source_id": "PMS-AFR-209",
  "purpose": "Verification of logging all status changes",
  "preconditions": "Status changes.",
  "action_or_input": "Search Audit Logs for 'Application ID' and 'Old Status/Status'.",
  "expected_result": "Changes are logged."
 },
 {
  "test_id": "TEST-CFR-024-3",
  "source_id": "PMS-AFR-210",
  "purpose": "Verification of logging all document modifications",
  "preconditions": "Document modified.",
  "action_or_input": "Search Audit Logs for 'Doc ID'.",
  "expected_result": "Modification is logged."
 },
 {
  "test_id": "TEST-CFR-024-4",
  "source_id": "PMS-AFR-211",
  "purpose": "Verification of audit logs including user ID, action type, timestamp, app ID, prev state, new state",
  "preconditions": "Action performed.",
  "action_or_input": "Inspect a specific log entry in detail.",
  "expected_result": "All 6 required fields are present."
 },
 {
  "test_id": "TEST-CFR-024-5",
  "source_id": "PMS-AFR-212",
  "purpose": "Verification of creating immutable audit records for critical operations",
  "preconditions": "Critical operation occurs (e.g., Budget Approval).",
  "action_or_input": "Attempt to modify the audit log entry.",
  "expected_result": "Modification is rejected/immutable."
 }
]
```
