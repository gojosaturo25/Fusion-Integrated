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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 65 to 72 of 204; write exactly these test cases into tests/a8/fr/test_fr_p09.py.
```json
[
 {
  "test_id": "TEST-CFR-011-5",
  "source_id": "PMS-AFR-095",
  "purpose": "Verify escalation to higher authority on cost threshold exceedance",
  "preconditions": "Total calculated budget exceeds the configured limit.",
  "action_or_input": "Attempt to approve the budget.",
  "expected_result": "The system routes/escalates the case to the higher authority instead of allowing approval."
 },
 {
  "test_id": "TEST-CFR-011-6",
  "source_id": "PMS-AFR-096",
  "purpose": "Verify restriction of budget approval for non-Approved status",
  "preconditions": "Application status is 'Submitted' (not Approved).",
  "action_or_input": "Director attempts to approve the associated budget.",
  "expected_result": "The system prevents approval with an error message."
 },
 {
  "test_id": "TEST-CFR-011-7",
  "source_id": "PMS-AFR-097",
  "purpose": "Verify validation of budget availability before approval",
  "preconditions": "Budget data includes an 'Available' flag set to false.",
  "action_or_input": "Director attempts to approve the budget.",
  "expected_result": "The system prevents approval and indicates insufficient availability."
 },
 {
  "test_id": "TEST-CFR-011-8",
  "source_id": "PMS-AFR-098",
  "purpose": "Verify logging of financial transactions with authorization info",
  "preconditions": "Budget approval is executed.",
  "action_or_input": "Access the Audit Logs for Financial Transactions.",
  "expected_result": "The log includes transaction details and the authorizing level."
 },
 {
  "test_id": "TEST-CFR-012-0",
  "source_id": "PMS-AFR-099",
  "purpose": "Verify Attorney preparation of filing package",
  "preconditions": "Application is ready for external filing.",
  "action_or_input": "Attorney navigates to 'File Application'.",
  "expected_result": "The system allows preparation of the application package."
 },
 {
  "test_id": "TEST-CFR-012-1",
  "source_id": "PMS-AFR-100",
  "purpose": "Verify validation of filing format compliance (if rules exist)",
  "preconditions": "Filing package includes invalid format for a specific office.",
  "action_or_input": "Submit the package.",
  "expected_result": "If valid validation rules exist, the system flags non-compliance."
 },
 {
  "test_id": "TEST-CFR-012-2",
  "source_id": "PMS-AFR-101",
  "purpose": "Verify recording of Indian Patent Office submission",
  "preconditions": "Attorney prepares the package.",
  "action_or_input": "Record the submission to Indian Patent Office.",
  "expected_result": "The system logs the submission details."
 },
 {
  "test_id": "TEST-CFR-012-3",
  "source_id": "PMS-AFR-102",
  "purpose": "Verify recording of International Patent Office submission",
  "preconditions": "Attorney prepares the package.",
  "action_or_input": "Record the submission to an international office (e.g., WIPO).",
  "expected_result": "The system logs the submission details."
 }
]
```
