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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 9 to 16 of 204; write exactly these test cases into tests/a8/fr/test_fr_p02.py.
```json
[
 {
  "test_id": "TEST-CFR-005-0",
  "source_id": "PMS-AFR-038",
  "purpose": "Verify complete application submission by Applicant",
  "preconditions": "Applicant is not currently involved in any active filing workflow.",
  "action_or_input": "Submit a patent application form with all required fields: title, abstract, claims, and documents.",
  "expected_result": "Submission is accepted and the application record is created."
 },
 {
  "test_id": "TEST-CFR-005-1",
  "source_id": "PMS-AFR-039",
  "purpose": "Verify rejection of non-PDF documents",
  "preconditions": "Applicant attempts to upload a DOCX file as application documentation.",
  "action_or_input": "Upload the document and attempt to proceed with submission.",
  "expected_result": "The system rejects the document and displays an error message stating it must be PDF."
 },
 {
  "test_id": "TEST-CFR-005-2",
  "source_id": "PMS-AFR-040",
  "purpose": "Verify rejection of oversized documents (>50 MB)",
  "preconditions": "Applicant attempts to upload a document that is 51 MB in size.",
  "action_or_input": "Upload the document and attempt to proceed with submission.",
  "expected_result": "The system rejects the document and displays an error message stating it exceeds 50 MB."
 },
 {
  "test_id": "TEST-CFR-005-3",
  "source_id": "PMS-AFR-041",
  "purpose": "Verify malware validation on submission",
  "preconditions": "Applicant attempts to upload a document containing known malicious code.",
  "action_or_input": "Upload the file and attempt to proceed with submission.",
  "expected_result": "The system rejects the document and displays a warning about undetected malware/threats."
 },
 {
  "test_id": "TEST-CFR-005-4",
  "source_id": "PMS-AFR-042",
  "purpose": "Verify rejection of incomplete application data",
  "preconditions": "Applicant submits an application missing the 'Claims' section.",
  "action_or_input": "Submit the application and attempt to proceed.",
  "expected_result": "The system prevents submission with a validation error listing missing required fields."
 },
 {
  "test_id": "TEST-CFR-005-5",
  "source_id": "PMS-AFR-043",
  "purpose": "Verify document sensitivity classification",
  "preconditions": "Application submission is successful.",
  "action_or_input": "View the application metadata in 'Submitted' state.",
  "expected_result": "Document metadata displays classified sensitivity levels (e.g., Internal, Confidential)."
 },
 {
  "test_id": "TEST-CFR-005-6",
  "source_id": "PMS-AFR-044",
  "purpose": "Verify unique Application ID assignment",
  "preconditions": "An application is submitted for the first time.",
  "action_or_input": "Retrieve the created application record.",
  "expected_result": "A unique alphanumeric Application ID is generated and displayed."
 },
 {
  "test_id": "TEST-CFR-005-7",
  "source_id": "PMS-AFR-045",
  "purpose": "Verify application status set to 'Submitted'",
  "preconditions": "Application submission is accepted.",
  "action_or_input": "Check the current state of the newly created application.",
  "expected_result": "The application status is updated to 'Submitted'."
 }
]
```
