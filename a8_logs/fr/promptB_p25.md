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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 193 to 200 of 204; write exactly these test cases into tests/a8/fr/test_fr_p25.py.
```json
[
 {
  "test_id": "TEST-CFR-028-1",
  "source_id": "PMS-AFR-222",
  "purpose": "Verification of allowing multiple Directors to handle reviews based on expertise domains",
  "preconditions": "Multiple domains exist.",
  "action_or_input": "Check Director assignments for different applications.",
  "expected_result": "Different Directors can handle applications in different domains."
 },
 {
  "test_id": "TEST-CFR-028-2",
  "source_id": "PMS-AFR-223",
  "purpose": "Verification of allowing multiple Attorneys from approved panels to conduct legal assessments",
  "preconditions": "Multiple Attorneys exist.",
  "action_or_input": "Check Attorney assignments for a complex application.",
  "expected_result": "Multiple Attorneys can be assigned/appointed if needed."
 },
 {
  "test_id": "TEST-CFR-028-3",
  "source_id": "PMS-AFR-224",
  "purpose": "Verification of allowing multiple Applicants to submit patent applications",
  "preconditions": "System is active.",
  "action_or_input": "Submit applications from distinct user IDs.",
  "expected_result": "Multiple applications are accepted."
 },
 {
  "test_id": "TEST-CFR-028-4",
  "source_id": "PMS-AFR-225",
  "purpose": "Verification of enforcing status-driven handling with valid transitions",
  "preconditions": "Application is in an invalid state or wrong transition attempted.",
  "action_or_input": "Attempt to change status from 'Submitted' directly to 'Filed'.",
  "expected_result": "Transition is denied."
 },
 {
  "test_id": "TEST-CFR-028-5",
  "source_id": "PMS-AFR-226",
  "purpose": "Verification of support for escalation mechanisms for delayed actions",
  "preconditions": "Action is delayed beyond threshold.",
  "action_or_input": "Check system response to delay.",
  "expected_result": "Escalation logic triggers."
 },
 {
  "test_id": "TEST-CFR-028-6",
  "source_id": "PMS-AFR-227",
  "purpose": "Verification of permitting parallel processing only where explicitly allowed",
  "preconditions": "Parallel process defined in config.",
  "action_or_input": "Attempt to handle two conflicting actions simultaneously if not defined.",
  "expected_result": "System restricts behavior based on explicit rules."
 },
 {
  "test_id": "TEST-CFR-029-0",
  "source_id": "PMS-AFR-228",
  "purpose": "Verification of treating patent-office integration as external unless PMS records details",
  "preconditions": "Integration configured.",
  "action_or_input": "Submit to Patent Office.",
  "expected_result": "System acts as a client; success/failure is only recorded as metadata."
 },
 {
  "test_id": "TEST-CFR-029-1",
  "source_id": "PMS-AFR-229",
  "purpose": "Verification of treating financial-system integration as external unless PMS records metadata",
  "preconditions": "Integration configured.",
  "action_or_input": "Execute payment.",
  "expected_result": "System records transaction details but does not own the funds."
 }
]
```
