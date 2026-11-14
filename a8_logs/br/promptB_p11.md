You are given:
1. the frozen A8_BASE Fusion implementation, and
2. the frozen BR_DESIGN.json.
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
- Store generated tests only under tests/a8/br/.
If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.

The frozen BR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 81 to 81 of 81; write exactly these test cases into tests/a8/br/test_br_p11.py.
```json
[
 {
  "test_id": "BR-PMS-146",
  "source_id": "BR-PMS-146",
  "purpose": "Verify PMS restricts Applicant review of office-action responses to applicable process conditions.",
  "preconditions": "Process configured: 'Attorney Only'. Office Action received. User (Applicant) attempts to review/approve response.",
  "action_or_input": "User selects 'Approve Response' in the interface.",
  "expected_result": "Action denied; system returns error stating Applicant review/approval required only when applicable process dictates it.",
  "test_type": "Acceptance"
 }
]
```
