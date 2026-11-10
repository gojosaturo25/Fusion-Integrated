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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 41 to 48 of 204; write exactly these test cases into tests/a8/fr/test_fr_p06.py.
```json
[
 {
  "test_id": "TEST-CFR-008-4",
  "source_id": "PMS-AFR-070",
  "purpose": "Verify restart of review cycle after resubmission",
  "preconditions": "Application is resubmitted successfully.",
  "action_or_input": "View the application workflow status.",
  "expected_result": "The system initiates a new review cycle."
 },
 {
  "test_id": "TEST-CFR-008-5",
  "source_id": "PMS-AFR-071",
  "purpose": "Verify version control for revised applications",
  "preconditions": "An application has been resubmitted.",
  "action_or_input": "Navigate to document management for the application.",
  "expected_result": "A new document version is recorded as V2 or higher with prior versions archived."
 },
 {
  "test_id": "TEST-CFR-008-6",
  "source_id": "PMS-AFR-072",
  "purpose": "Verify status change to 'Expired' on deadline expiration",
  "preconditions": "Application is awaiting revision and the 60-day deadline has passed without resubmission.",
  "action_or_input": "Check the application status record.",
  "expected_result": "The application status is automatically updated to 'Expired'.",
  "test_type": "UC-05 Alternative A1"
 },
 {
  "test_id": "TEST-CFR-009-0",
  "source_id": "PMS-AFR-074",
  "purpose": "Verify restriction of attorney assignment to PCC_ADMIN only",
  "preconditions": "Director attempts to assign an Attorney directly.",
  "action_or_input": "Submit an 'Assign Attorney' command from the Director dashboard.",
  "expected_result": "The system denies access and displays an error that only PCC_ADMIN can perform this action."
 },
 {
  "test_id": "TEST-CFR-009-1",
  "source_id": "PMS-AFR-075",
  "purpose": "Verify requirement of approved panel for attorney selection",
  "preconditions": "An approved application is selected.",
  "action_or_input": "PCC_ADMIN attempts to assign an Attorney who is not on the approved panel (except if exception exists).",
  "expected_result": "The system prevents assignment unless a valid institutional exception is recorded."
 },
 {
  "test_id": "TEST-CFR-009-2",
  "source_id": "PMS-AFR-076",
  "purpose": "Verify attorney expertise matching during assignment",
  "preconditions": "Application domain is 'Biology'. Attorney A (Biology) and B (Chemistry) are eligible.",
  "action_or_input": "Execute attorney assignment process.",
  "expected_result": "The system prioritizes or selects Attorney A based on domain expertise."
 },
 {
  "test_id": "TEST-CFR-009-3",
  "source_id": "PMS-AFR-077",
  "purpose": "Verify attorney workload consideration during assignment",
  "preconditions": "Attorney A has high workload; Attorney B has low workload. Both have correct expertise.",
  "action_or_input": "Execute attorney assignment process.",
  "expected_result": "The system favors assignment to Attorney B due to lower workload."
 },
 {
  "test_id": "TEST-CFR-009-4",
  "source_id": "PMS-AFR-078",
  "purpose": "Verify conflict-of-interest check before attorney assignment",
  "preconditions": "Attorney C has a prior relationship with an inventor on the application.",
  "action_or_input": "PCC_ADMIN attempts to assign Attorney C to the application.",
  "expected_result": "The system prevents assignment and flags a Conflict of Interest."
 }
]
```
