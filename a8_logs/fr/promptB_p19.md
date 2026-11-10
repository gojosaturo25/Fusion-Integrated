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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 145 to 152 of 204; write exactly these test cases into tests/a8/fr/test_fr_p19.py.
```json
[
 {
  "test_id": "TEST-CFR-021-3",
  "source_id": "PMS-AFR-175",
  "purpose": "Verification of calculation/monitoring of maintenance-fee deadlines (if data available)",
  "preconditions": "Patent Granted, jurisdiction data available.",
  "action_or_input": "View the timeline dashboard.",
  "expected_result": "Maintenance fee deadline is calculated and displayed."
 },
 {
  "test_id": "TEST-CFR-021-4",
  "source_id": "PMS-AFR-176",
  "purpose": "Verification of generating alert 30 days before deadline (if applicable)",
  "preconditions": "Deadline is active.",
  "action_or_input": "Check notifications at T-30.",
  "expected_result": "Alert message is generated."
 },
 {
  "test_id": "TEST-CFR-021-5",
  "source_id": "PMS-AFR-177",
  "purpose": "Verification of generating alert 15 days before deadline (if applicable)",
  "preconditions": "Deadline is active.",
  "action_or_input": "Check notifications at T-15.",
  "expected_result": "Alert message is generated."
 },
 {
  "test_id": "TEST-CFR-021-6",
  "source_id": "PMS-AFR-178",
  "purpose": "Verification of generating alert 5 days before deadline (if applicable)",
  "preconditions": "Deadline is active.",
  "action_or_input": "Check notifications at T-5.",
  "expected_result": "Alert message is generated."
 },
 {
  "test_id": "TEST-CFR-021-7",
  "source_id": "PMS-AFR-179",
  "purpose": "Verification of sending deadline notifications to stakeholders",
  "preconditions": "Alert conditions are met.",
  "action_or_input": "Monitor communication logs.",
  "expected_result": "Notifications are sent to relevant parties."
 },
 {
  "test_id": "TEST-CFR-021-8",
  "source_id": "PMS-AFR-180",
  "purpose": "Verification of escalation for missed deadlines (configured chain)",
  "preconditions": "Deadline is missed.",
  "action_or_input": "Check status of the process flow.",
  "expected_result": "System triggers the configured escalation path."
 },
 {
  "test_id": "TEST-CFR-021-9",
  "source_id": "PMS-AFR-181",
  "purpose": "Verification of logging deadline tracking activities",
  "preconditions": "Deadline monitoring is active.",
  "action_or_input": "Access Audit Logs for 'Deadline' entries.",
  "expected_result": "Activities are logged."
 },
 {
  "test_id": "TEST-CFR-022-0",
  "source_id": "PMS-AFR-182",
  "purpose": "Verification of generating application status/progress reports (PCC_ADMIN/Director)",
  "preconditions": "User has role.",
  "action_or_input": "Generate 'Application Status' report.",
  "expected_result": "Report is generated."
 }
]
```
