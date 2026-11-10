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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 153 to 160 of 204; write exactly these test cases into tests/a8/fr/test_fr_p20.py.
```json
[
 {
  "test_id": "TEST-CFR-022-1",
  "source_id": "PMS-AFR-183",
  "purpose": "Verification of generating financial/budget reports (PCC_ADMIN/Director)",
  "preconditions": "User has role.",
  "action_or_input": "Generate 'Budget Report'.",
  "expected_result": "Report is generated."
 },
 {
  "test_id": "TEST-CFR-022-2",
  "source_id": "PMS-AFR-184",
  "purpose": "Verification of generating deadline/pending action reports (PCC_ADMIN/Director)",
  "preconditions": "User has role.",
  "action_or_input": "Generate 'Deadline Report'.",
  "expected_result": "Report is generated."
 },
 {
  "test_id": "TEST-CFR-022-3",
  "source_id": "PMS-AFR-185",
  "purpose": "Verification of generating inventor/co-inventor reports (PCC_ADMIN/Director)",
  "preconditions": "User has role.",
  "action_or_input": "Generate 'Inventor Report'.",
  "expected_result": "Report is generated."
 },
 {
  "test_id": "TEST-CFR-022-4",
  "source_id": "PMS-AFR-186",
  "purpose": "Verification of generating patent portfolio analysis reports (PCC_ADMIN/Director)",
  "preconditions": "User has role.",
  "action_or_input": "Generate 'Portfolio Analysis'.",
  "expected_result": "Report is generated."
 },
 {
  "test_id": "TEST-CFR-022-5",
  "source_id": "PMS-AFR-187",
  "purpose": "Verification of generating workload/assignment reports (PCC_ADMIN/Director)",
  "preconditions": "User has role.",
  "action_or_input": "Generate 'Workload Report'.",
  "expected_result": "Report is generated."
 },
 {
  "test_id": "TEST-CFR-022-6",
  "source_id": "PMS-AFR-188",
  "purpose": "Verification of scheduling reports (authorized users)",
  "preconditions": "User has role.",
  "action_or_input": "Schedule a report for a future time.",
  "expected_result": "Schedule is created."
 },
 {
  "test_id": "TEST-CFR-022-7",
  "source_id": "PMS-AFR-189",
  "purpose": "Verification of exporting reports (authorized users)",
  "preconditions": "Report is generated.",
  "action_or_input": "Click 'Export' button.",
  "expected_result": "File is downloaded/available for export."
 },
 {
  "test_id": "TEST-CFR-022-8",
  "source_id": "PMS-AFR-190",
  "purpose": "Verification of customizing reports (authorized users)",
  "preconditions": "Report is generated.",
  "action_or_input": "Modify report filters/parameters.",
  "expected_result": "Customization is applied."
 }
]
```
