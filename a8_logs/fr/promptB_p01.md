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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 1 to 8 of 204; write exactly these test cases into tests/a8/fr/test_fr_p01.py.
```json
[
 {
  "test_id": "TEST-CFR-001-0",
  "source_id": "PMS-AFR-010",
  "purpose": "Verify application tracking by Applicant",
  "preconditions": "An applicant with valid credentials logs into PMS.",
  "action_or_input": "Navigate to 'My Applications' view.",
  "expected_result": "A list of the applicant's patent applications is displayed with current status and progress indicators."
 },
 {
  "test_id": "TEST-CFR-001-1",
  "source_id": "PMS-AFR-016",
  "purpose": "Verify report viewing by Applicant",
  "preconditions": "An applicant with valid credentials logs into PMS.",
  "action_or_input": "Navigate to 'Reports' and select a specific application ID.",
  "expected_result": "A report containing details of the selected patent application is displayed."
 },
 {
  "test_id": "TEST-CFR-002-0",
  "source_id": "PMS-AFR-023",
  "purpose": "Verify workflow oversight by Director",
  "preconditions": "A Director with valid credentials logs into PMS.",
  "action_or_input": "Navigate to 'Assigned Applications' view.",
  "expected_result": "The application list includes only applications assigned to this specific Director with relevant workflow details."
 },
 {
  "test_id": "TEST-CFR-003-0",
  "source_id": "PMS-AFR-026",
  "purpose": "Verify conflict-of-interest monitoring by PCC_ADMIN",
  "preconditions": "PCC_ADMIN has a co-inventorship with an inventor listed on an application.",
  "action_or_input": "Attempt to view the assigned application in 'Workflow Exceptions' section.",
  "expected_result": "The system flags the conflict-of-interest case requiring resolution."
 },
 {
  "test_id": "TEST-CFR-003-1",
  "source_id": "PMS-AFR-027",
  "purpose": "Verify configuration management by PCC_ADMIN",
  "preconditions": "PCC_ADMIN has valid credentials.",
  "action_or_input": "Navigate to 'System Configuration' and select 'User Roles'.",
  "expected_result": "A list of assigned roles is displayed with edit permissions available."
 },
 {
  "test_id": "TEST-CFR-003-2",
  "source_id": "PMS-AFR-029",
  "purpose": "Verify escalation handling by PCC_ADMIN",
  "preconditions": "An application has missed its review deadline.",
  "action_or_input": "Navigate to 'Workflow Exceptions' and select an escalated case.",
  "expected_result": "Case details are displayed with a path for resolution."
 },
 {
  "test_id": "TEST-CFR-003-3",
  "source_id": "PMS-AFR-030",
  "purpose": "Verify attorney panel management by PCC_ADMIN",
  "preconditions": "PCC_ADMIN has valid credentials.",
  "action_or_input": "Navigate to 'Attorney Panels' and add a new attorney.",
  "expected_result": "The new attorney is added to the approved panel list."
 },
 {
  "test_id": "TEST-CFR-004-0",
  "source_id": "PMS-AFR-037",
  "purpose": "Verify legal advice recording by Attorney",
  "preconditions": "An application has status 'Attorney Assigned'.",
  "action_or_input": "Navigate to 'Case Notes' and input a detailed legal opinion.",
  "expected_result": "The legal opinion is recorded in the application history."
 }
]
```
