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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 89 to 96 of 204; write exactly these test cases into tests/a8/fr/test_fr_p12.py.
```json
[
 {
  "test_id": "TEST-CFR-014-2",
  "source_id": "PMS-AFR-118",
  "purpose": "Verify Attorney preparation of draft responses",
  "preconditions": "Office Action is open for review.",
  "action_or_input": "Attorney creates a draft response.",
  "expected_result": "A draft response document is created."
 },
 {
  "test_id": "TEST-CFR-014-3",
  "source_id": "PMS-AFR-119",
  "purpose": "Verify Applicant review/approval of office-action responses (if required)",
  "preconditions": "Applicable process requires Applicant approval.",
  "action_or_input": "Applicant reviews and approves the draft response.",
  "expected_result": "The system records Applicant approval."
 },
 {
  "test_id": "TEST-CFR-014-4",
  "source_id": "PMS-AFR-120",
  "purpose": "Verify Attorney finalization of office-action responses",
  "preconditions": "Applicant has approved the draft.",
  "action_or_input": "Attorney marks the response as 'Finalized'.",
  "expected_result": "The system updates status to Finalized."
 },
 {
  "test_id": "TEST-CFR-014-5",
  "source_id": "PMS-AFR-121",
  "purpose": "Verify recording of office-action response submission within deadline",
  "preconditions": "Response is finalized.",
  "action_or_input": "Submit the finalized response.",
  "expected_result": "Submission details are recorded and timestamped."
 },
 {
  "test_id": "TEST-CFR-014-6",
  "source_id": "PMS-AFR-122",
  "purpose": "Verify recording of extension requests for additional response time",
  "preconditions": "Deadline is imminent.",
  "action_or_input": "Attorney submits an extension request.",
  "expected_result": "Extension details are recorded if the process allows it."
 },
 {
  "test_id": "TEST-CFR-014-7",
  "source_id": "PMS-AFR-123",
  "purpose": "Verify tracking of response submission status",
  "preconditions": "Response has been submitted.",
  "action_or_input": "View the application status regarding this Office Action.",
  "expected_result": "Status reflects 'Submitted' or similar."
 },
 {
  "test_id": "TEST-CFR-014-8",
  "source_id": "PMS-AFR-124",
  "purpose": "Verify automation of deadline tracking for responses (if data available)",
  "preconditions": "Deadline is calculable based on received action.",
  "action_or_input": "Monitor system alerts for the response.",
  "expected_result": "System automatically generates and displays deadline countdowns."
 },
 {
  "test_id": "TEST-CFR-015-0",
  "source_id": "PMS-AFR-125",
  "purpose": "Verify withdrawal of applications before filing stage (Pre-Filing)",
  "preconditions": "Application status is 'Submitted' (and withdrawal allowed).",
  "action_or_input": "Applicant submits a withdrawal request.",
  "expected_result": "Withdrawal is processed."
 }
]
```
