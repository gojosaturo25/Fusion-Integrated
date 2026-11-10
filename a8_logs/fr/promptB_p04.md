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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 25 to 32 of 204; write exactly these test cases into tests/a8/fr/test_fr_p04.py.
```json
[
 {
  "test_id": "TEST-CFR-006-5",
  "source_id": "PMS-AFR-054",
  "purpose": "Verify prevention of self-review by Director",
  "preconditions": "Director X lists himself as an inventor on Application Y.",
  "action_or_input": "Director X attempts to view or process Application Y.",
  "expected_result": "The system prevents access and denies the Director from handling this application."
 },
 {
  "test_id": "TEST-CFR-006-6",
  "source_id": "PMS-AFR-055",
  "purpose": "Verify prevention of self-review by PCC_ADMIN",
  "preconditions": "PCC_ADMIN is listed as an inventor on an application.",
  "action_or_input": "Attempt to view the specific application details.",
  "expected_result": "The system restricts viewing permissions for this application."
 },
 {
  "test_id": "TEST-CFR-006-7",
  "source_id": "PMS-AFR-056",
  "purpose": "Verify status update to 'Under Review'",
  "preconditions": "An assignment is completed.",
  "action_or_input": "Check the application status field.",
  "expected_result": "The application status updates from 'Submitted' to 'Under Review'."
 },
 {
  "test_id": "TEST-CFR-006-8",
  "source_id": "PMS-AFR-057",
  "purpose": "Verify notification of assigned Director",
  "preconditions": "Application is assigned to a Director.",
  "action_or_input": "Monitor the assigned Director's communication channel.",
  "expected_result": "A notification regarding the assignment and initiation of the review timeline is generated."
 },
 {
  "test_id": "TEST-CFR-007-0",
  "source_id": "PMS-AFR-058",
  "purpose": "Verify Director access to application details",
  "preconditions": "Application status is 'Under Review'.",
  "action_or_input": "Director navigates to the assigned application.",
  "expected_result": "Director views full application details, documents, and supporting materials."
 },
 {
  "test_id": "TEST-CFR-007-1",
  "source_id": "PMS-AFR-059",
  "purpose": "Verify valid review decision selection (Approve/Reject/Revision)",
  "preconditions": "Director is reviewing an application.",
  "action_or_input": "Select a decision from the dropdown: Approve, Reject, or Needs Revision.",
  "expected_result": "The system accepts exactly one of these three decisions."
 },
 {
  "test_id": "TEST-CFR-007-2",
  "source_id": "PMS-AFR-060",
  "purpose": "Verify minimum justification length (50 characters)",
  "preconditions": "Director attempts to submit a decision.",
  "action_or_input": "Submit a decision with a justification containing fewer than 50 characters.",
  "expected_result": "The system prevents submission and prompts for additional justification text."
 },
 {
  "test_id": "TEST-CFR-007-3",
  "source_id": "PMS-AFR-061",
  "purpose": "Verify enforcement of 15-day review deadline",
  "preconditions": "Application is 'Under Review' and current time exceeds the review deadline.",
  "action_or_input": "Attempt to view submission controls for this application.",
  "expected_result": "The system prevents further action or logs a status of 'Overdue Review'.",
  "test_type": "WF-02 approval-rejected path"
 }
]
```
