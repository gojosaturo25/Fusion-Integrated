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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 81 to 88 of 204; write exactly these test cases into tests/a8/fr/test_fr_p11.py.
```json
[
 {
  "test_id": "TEST-CFR-013-4",
  "source_id": "PMS-AFR-110",
  "purpose": "Verify requirement of explicit renewal decision before deadline",
  "preconditions": "Maintenance deadline is approaching.",
  "action_or_input": "Skip the renewal decision process.",
  "expected_result": "The system prevents proceeding past the deadline without a decision."
 },
 {
  "test_id": "TEST-CFR-013-5",
  "source_id": "PMS-AFR-111",
  "purpose": "Verify Attorney seeking renewal decision from Director",
  "preconditions": "Renewal deadline is active.",
  "action_or_input": "Attorney clicks 'Request Renewal Decision'.",
  "expected_result": "A request form or workflow to the Director is triggered."
 },
 {
  "test_id": "TEST-CFR-013-6",
  "source_id": "PMS-AFR-112",
  "purpose": "Verify Director decision (Renew/Do Not Renew)",
  "preconditions": "Renewal request received by Director.",
  "action_or_input": "Director selects 'Renew' or 'Do Not Renew'.",
  "expected_result": "The system accepts and records one of these decisions."
 },
 {
  "test_id": "TEST-CFR-013-7",
  "source_id": "PMS-AFR-113",
  "purpose": "Verify Attorney recording of maintenance action/transaction upon renewal approval",
  "preconditions": "Director decision is 'Renew'.",
  "action_or_input": "Attorney processes the payment and updates the status.",
  "expected_result": "The transaction, status, and action are recorded."
 },
 {
  "test_id": "TEST-CFR-013-8",
  "source_id": "PMS-AFR-114",
  "purpose": "Verify maintenance of renewal history",
  "preconditions": "Renewal was executed previously.",
  "action_or_input": "View 'Maintenance History'.",
  "expected_result": "Previous renewals are listed with details."
 },
 {
  "test_id": "TEST-CFR-013-9",
  "source_id": "PMS-AFR-115",
  "purpose": "Verify scheduling of next maintenance cycle",
  "preconditions": "One renewal cycle is completed.",
  "action_or_input": "Check the next scheduled action date.",
  "expected_result": "The system schedules the next maintenance cycle."
 },
 {
  "test_id": "TEST-CFR-014-0",
  "source_id": "PMS-AFR-116",
  "purpose": "Verify recording of office actions received",
  "preconditions": "Patent Office sends an Office Action.",
  "action_or_input": "Navigate to 'Office Actions'.",
  "expected_result": "The Office Action is recorded in the system."
 },
 {
  "test_id": "TEST-CFR-014-1",
  "source_id": "PMS-AFR-117",
  "purpose": "Verify Attorney review of recorded office actions",
  "preconditions": "Office Action is recorded.",
  "action_or_input": "Attorney views the action details.",
  "expected_result": "Attorney can review and analyze the content."
 }
]
```
