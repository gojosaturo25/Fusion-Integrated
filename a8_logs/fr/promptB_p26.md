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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 201 to 204 of 204; write exactly these test cases into tests/a8/fr/test_fr_p26.py.
```json
[
 {
  "test_id": "TEST-CFR-029-2",
  "source_id": "PMS-AFR-230",
  "purpose": "Verification of treating document-management-system integration as external unless PMS stores metadata",
  "preconditions": "Integration configured.",
  "action_or_input": "Upload to Doc Mgmt System.",
  "expected_result": "System records version/metadata but relies on external storage."
 },
 {
  "test_id": "TEST-CFR-029-3",
  "source_id": "PMS-AFR-231",
  "purpose": "Verification of treating external prior-art databases as query sources (not owned)",
  "preconditions": "Search executed.",
  "action_or_input": "Check source of data retrieved.",
  "expected_result": "Data is identified as external/proprietary."
 },
 {
  "test_id": "TEST-CFR-029-4",
  "source_id": "PMS-AFR-232",
  "purpose": "Verification of not treating external patent office filing success as internally controlled beyond recording details",
  "preconditions": "External office grants filing.",
  "action_or_input": "Check PMS status upon external confirmation.",
  "expected_result": "PMS records the event but does not guarantee control over the result."
 },
 {
  "test_id": "TEST-CFR-030-0",
  "source_id": "PMS-AFR-236",
  "purpose": "Verification of allowing Director to reject a proposed budget and record outcome",
  "preconditions": "Budget submitted.",
  "action_or_input": "Director selects 'Reject' and records reason.",
  "expected_result": "Rejection is recorded."
 }
]
```
