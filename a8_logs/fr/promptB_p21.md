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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 161 to 168 of 204; write exactly these test cases into tests/a8/fr/test_fr_p21.py.
```json
[
 {
  "test_id": "TEST-CFR-022-9",
  "source_id": "PMS-AFR-191",
  "purpose": "Verification of logging report access for audit (authorized users)",
  "preconditions": "Report is viewed.",
  "action_or_input": "Check Audit Logs.",
  "expected_result": "Access event is logged."
 },
 {
  "test_id": "TEST-CFR-022-10",
  "source_id": "PMS-AFR-237",
  "purpose": "Verification of providing dashboards within reporting scope",
  "preconditions": "User has role.",
  "action_or_input": "Navigate to 'Dashboards'.",
  "expected_result": "Dashboard is visible."
 },
 {
  "test_id": "TEST-CFR-022-11",
  "source_id": "PMS-AFR-238",
  "purpose": "Verification of providing historical data analysis within reporting scope",
  "preconditions": "Historical data exists.",
  "action_or_input": "Query time-series report.",
  "expected_result": "Analysis is displayed."
 },
 {
  "test_id": "TEST-CFR-022-12",
  "source_id": "PMS-AFR-239",
  "purpose": "Verification of providing trend reporting within reporting scope",
  "preconditions": "Trend data exists.",
  "action_or_input": "View 'Trend Analysis'.",
  "expected_result": "Trends are displayed."
 },
 {
  "test_id": "TEST-CFR-023-0",
  "source_id": "PMS-AFR-192",
  "purpose": "Verification of triggering notification for application submission",
  "preconditions": "Application is submitted.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-1",
  "source_id": "PMS-AFR-193",
  "purpose": "Verification of triggering notification for application status change",
  "preconditions": "Status changes.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-2",
  "source_id": "PMS-AFR-194",
  "purpose": "Verification of triggering notification for assignment to Director",
  "preconditions": "Assignment occurs.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 },
 {
  "test_id": "TEST-CFR-023-3",
  "source_id": "PMS-AFR-195",
  "purpose": "Verification of triggering notification for assignment to Attorney",
  "preconditions": "Assignment occurs.",
  "action_or_input": "Check email logs.",
  "expected_result": "Notification is triggered."
 }
]
```
