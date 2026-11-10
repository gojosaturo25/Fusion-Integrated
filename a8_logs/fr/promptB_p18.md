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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 137 to 144 of 204; write exactly these test cases into tests/a8/fr/test_fr_p18.py.
```json
[
 {
  "test_id": "TEST-CFR-020-2",
  "source_id": "PMS-AFR-167",
  "purpose": "Verification of requirement for grounds and justification for appeal",
  "preconditions": "Appeal form is open.",
  "action_or_input": "Submit an appeal with empty justification.",
  "expected_result": "System requires justification input."
 },
 {
  "test_id": "TEST-CFR-020-3",
  "source_id": "PMS-AFR-168",
  "purpose": "Verification of Director review of appeals and documentation",
  "preconditions": "Appeal is filed.",
  "action_or_input": "Director views the appeal details.",
  "expected_result": "Director can review grounds and submit supporting docs."
 },
 {
  "test_id": "TEST-CFR-020-4",
  "source_id": "PMS-AFR-169",
  "purpose": "Verification of Director choice (Uphold/Remand/Modify)",
  "preconditions": "Review is complete.",
  "action_or_input": "Director selects an appeal outcome.",
  "expected_result": "One of 'Uphold Rejection', 'Remand for Amendment', or 'Modify Decision' is selected."
 },
 {
  "test_id": "TEST-CFR-020-5",
  "source_id": "PMS-AFR-170",
  "purpose": "Verification of recording appeal outcomes",
  "preconditions": "Decision is made.",
  "action_or_input": "View the Case Outcome page.",
  "expected_result": "Outcome details are recorded."
 },
 {
  "test_id": "TEST-CFR-020-6",
  "source_id": "PMS-AFR-171",
  "purpose": "Verification of initiation of next applicable process step",
  "preconditions": "Appeal outcome is recorded.",
  "action_or_input": "Check the workflow status.",
  "expected_result": "System initiates the relevant next process."
 },
 {
  "test_id": "TEST-CFR-021-0",
  "source_id": "PMS-AFR-172",
  "purpose": "Verification of calculation/monitoring of Director review deadlines",
  "preconditions": "Application is 'Under Review'.",
  "action_or_input": "View the timeline dashboard.",
  "expected_result": "Deadline for review is calculated and displayed."
 },
 {
  "test_id": "TEST-CFR-021-1",
  "source_id": "PMS-AFR-173",
  "purpose": "Verification of calculation/monitoring of revision/resubmission deadlines",
  "preconditions": "Application is awaiting resubmission.",
  "action_or_input": "View the timeline dashboard.",
  "expected_result": "Deadline for revision is calculated and displayed."
 },
 {
  "test_id": "TEST-CFR-021-2",
  "source_id": "PMS-AFR-174",
  "purpose": "Verification of calculation/monitoring of office-action response deadlines (if data available)",
  "preconditions": "Office Action received, deadline calculable.",
  "action_or_input": "View the timeline dashboard.",
  "expected_result": "Deadline for response is calculated and displayed."
 }
]
```
