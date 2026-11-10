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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 121 to 128 of 204; write exactly these test cases into tests/a8/fr/test_fr_p16.py.
```json
[
 {
  "test_id": "TEST-CFR-018-1",
  "source_id": "PMS-AFR-151",
  "purpose": "Verify permission to upload new versions (role/status allowed)",
  "preconditions": "Applicant has 'Needs Revision' status.",
  "action_or_input": "Attempt to upload a new document.",
  "expected_result": "Upload is permitted."
 },
 {
  "test_id": "TEST-CFR-018-2",
  "source_id": "PMS-AFR-152",
  "purpose": "Verify assignment of automatic version numbers to new document versions",
  "preconditions": "New document is uploaded.",
  "action_or_input": "View the document header.",
  "expected_result": "Auto-generated version number (e.g., v3.0) appears."
 },
 {
  "test_id": "TEST-CFR-018-3",
  "source_id": "PMS-AFR-153",
  "purpose": "Verify archiving of previous document versions",
  "preconditions": "Versions exist in history.",
  "action_or_input": "Select an archived version.",
  "expected_result": "System confirms the version is in 'Archived' state."
 },
 {
  "test_id": "TEST-CFR-018-4",
  "source_id": "PMS-AFR-154",
  "purpose": "Verify access control for previous document versions (role/status rules)",
  "preconditions": "User has restricted role accessing an archived doc.",
  "action_or_input": "Attempt to view the document.",
  "expected_result": "Access is granted only if user role and status permit it."
 },
 {
  "test_id": "TEST-CFR-018-5",
  "source_id": "PMS-AFR-155",
  "purpose": "Verification of logging document modifications with user/timestamp",
  "preconditions": "Document is modified.",
  "action_or_input": "View the modification log.",
  "expected_result": "Log entry includes User ID and Timestamp."
 },
 {
  "test_id": "TEST-CFR-018-6",
  "source_id": "PMS-AFR-156",
  "purpose": "Verification of control based on role and application status",
  "preconditions": "User lacks required permission.",
  "action_or_input": "Attempt to access a confidential document.",
  "expected_result": "Access is denied."
 },
 {
  "test_id": "TEST-CFR-018-7",
  "source_id": "PMS-AFR-157",
  "purpose": "Verify restriction of document editing to 'Needs Revision' status for Applicants",
  "preconditions": "Application status is 'Submitted'.",
  "action_or_input": "Attempt by Applicant to edit the main application document.",
  "expected_result": "System prevents editing."
 },
 {
  "test_id": "TEST-CFR-019-0",
  "source_id": "PMS-AFR-158",
  "purpose": "Verify Applicant submission of licensing requests",
  "preconditions": "Application is in a state allowing licensing.",
  "action_or_input": "Applicant submits a Licensing Request form.",
  "expected_result": "Request is recorded."
 }
]
```
