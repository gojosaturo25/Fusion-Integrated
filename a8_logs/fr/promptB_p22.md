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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 169 to 176 of 204; write exactly these test cases into tests/a8/fr/test_fr_p22.py.
```json
[
 {
  "test_id": "TEST-CFR-023-4",
  "source_id": "PMS-AFR-196",
  "purpose": "Verification of triggering notification for review decisions",
  "preconditions": "Decision is made.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-5",
  "source_id": "PMS-AFR-197",
  "purpose": "Verification of triggering notification for budget approval/rejection",
  "preconditions": "Budget decision is made.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-6",
  "source_id": "PMS-AFR-198",
  "purpose": "Verification of triggering notification for filing confirmations",
  "preconditions": "Filing is recorded.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-7",
  "source_id": "PMS-AFR-199",
  "purpose": "Verification of triggering notification for office actions",
  "preconditions": "Office Action recorded.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-8",
  "source_id": "PMS-AFR-200",
  "purpose": "Verification of triggering notification for deadline reminders",
  "preconditions": "Deadline approaching.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-9",
  "source_id": "PMS-AFR-201",
  "purpose": "Verification of triggering notification for deadline escalations",
  "preconditions": "Deadline missed.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-10",
  "source_id": "PMS-AFR-202",
  "purpose": "Verification of triggering notification for maintenance-fee reminders",
  "preconditions": "Maintenance due.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-11",
  "source_id": "PMS-AFR-203",
  "purpose": "Verification of triggering notification for document updates",
  "preconditions": "Document updated.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 }
]
```
