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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 185 to 192 of 204; write exactly these test cases into tests/a8/fr/test_fr_p24.py.
```json
[
 {
  "test_id": "TEST-CFR-024-6",
  "source_id": "PMS-AFR-213",
  "purpose": "Verification of providing audit logs for compliance verification and forensic analysis",
  "preconditions": "Audit logs exist.",
  "action_or_input": "Access 'Compliance View'.",
  "expected_result": "Logs are accessible for verification."
 },
 {
  "test_id": "TEST-CFR-024-7",
  "source_id": "PMS-AFR-214",
  "purpose": "Verification of encryption at rest for PMS data (where implemented)",
  "preconditions": "Data is stored.",
  "action_or_input": "Perform physical inspection of storage media (if accessible) or check security config.",
  "expected_result": "Encryption confirmation exists."
 },
 {
  "test_id": "TEST-CFR-024-8",
  "source_id": "PMS-AFR-215",
  "purpose": "Verification of encryption in transit for PMS data (where implemented)",
  "preconditions": "Data is being transmitted.",
  "action_or_input": "Capture traffic or check network logs.",
  "expected_result": "Encrypted traffic is observed."
 },
 {
  "test_id": "TEST-CFR-025-0",
  "source_id": "PMS-AFR-216",
  "purpose": "Verification of requiring valid role assignments before access",
  "preconditions": "User has no PMS role.",
  "action_or_input": "Attempt to access any patent-management function.",
  "expected_result": "Access is denied."
 },
 {
  "test_id": "TEST-CFR-026-0",
  "source_id": "PMS-AFR-217",
  "purpose": "Verification of preventing attorney assignment until Director approval recorded",
  "preconditions": "Director has not approved the application.",
  "action_or_input": "Attempt to assign an Attorney.",
  "expected_result": "Assignment is blocked."
 },
 {
  "test_id": "TEST-CFR-026-1",
  "source_id": "PMS-AFR-218",
  "purpose": "Verification of preventing external filing until required approvals/budget allocated",
  "preconditions": "Budget is not approved.",
  "action_or_input": "Attempt to file externally.",
  "expected_result": "Filing is blocked."
 },
 {
  "test_id": "TEST-CFR-027-0",
  "source_id": "PMS-AFR-220",
  "purpose": "Verification of enforcing role-based access control (RBAC) for confidential info",
  "preconditions": "User has low clearance, data is confidential.",
  "action_or_input": "Attempt to view the document.",
  "expected_result": "Access is denied."
 },
 {
  "test_id": "TEST-CFR-028-0",
  "source_id": "PMS-AFR-221",
  "purpose": "Verification of maintaining exactly one active PCC_ADMIN as oversight role",
  "preconditions": "System state checked.",
  "action_or_input": "Query 'Admin Count'.",
  "expected_result": "Exactly 1 active PCC_ADMIN is found."
 }
]
```
