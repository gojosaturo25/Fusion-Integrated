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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 97 to 104 of 204; write exactly these test cases into tests/a8/fr/test_fr_p13.py.
```json
[
 {
  "test_id": "TEST-CFR-015-1",
  "source_id": "PMS-AFR-126",
  "purpose": "Verify validation of withdrawal eligibility based on status",
  "preconditions": "Application status is 'Under Review'.",
  "action_or_input": "Applicant attempts to withdraw.",
  "expected_result": "The system rejects withdrawal as it is not allowed for this status."
 },
 {
  "test_id": "TEST-CFR-015-2",
  "source_id": "PMS-AFR-127",
  "purpose": "Verify requirement of withdrawal reason",
  "preconditions": "Applicant attempts to withdraw.",
  "action_or_input": "Submit a request without a reason field populated.",
  "expected_result": "The system rejects the request and prompts for a reason."
 },
 {
  "test_id": "TEST-CFR-015-3",
  "source_id": "PMS-AFR-128",
  "purpose": "Verify support of recording co-inventor consent for withdrawal (if required)",
  "preconditions": "Application has multiple inventors and consent is required.",
  "action_or_input": "Complete the withdrawal form with consent signatures.",
  "expected_result": "Consent is recorded in the application history."
 },
 {
  "test_id": "TEST-CFR-015-4",
  "source_id": "PMS-AFR-129",
  "purpose": "Verify status update to 'Withdrawn' after permitted withdrawal",
  "preconditions": "Withdrawal is processed successfully.",
  "action_or_input": "Check application status record.",
  "expected_result": "Status updates to 'Withdrawn'."
 },
 {
  "test_id": "TEST-CFR-015-5",
  "source_id": "PMS-AFR-130",
  "purpose": "Verify removal of withdrawn applications from active queue",
  "preconditions": "Application is 'Withdrawn'.",
  "action_or_input": "Search the Active Queue.",
  "expected_result": "The application does not appear in the active queue."
 },
 {
  "test_id": "TEST-CFR-015-6",
  "source_id": "PMS-AFR-131",
  "purpose": "Verify maintenance of withdrawal history",
  "preconditions": "Application was withdrawn previously.",
  "action_or_input": "Access 'Withdrawal History' report.",
  "expected_result": "Details of the withdrawal are available."
 },
 {
  "test_id": "TEST-CFR-016-0",
  "source_id": "PMS-AFR-132",
  "purpose": "Verify management of multiple inventors by Applicant",
  "preconditions": "Applicant is preparing a new application.",
  "action_or_input": "Add three different inventor names.",
  "expected_result": "All three inventors are added to the list."
 },
 {
  "test_id": "TEST-CFR-016-1",
  "source_id": "PMS-AFR-133",
  "purpose": "Verify management of ownership shares for inventors",
  "preconditions": "Multiple inventors are listed.",
  "action_or_input": "Assign specific percentage shares to each inventor.",
  "expected_result": "Ownership percentages are recorded."
 }
]
```
