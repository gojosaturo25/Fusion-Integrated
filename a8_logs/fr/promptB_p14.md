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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 105 to 112 of 204; write exactly these test cases into tests/a8/fr/test_fr_p14.py.
```json
[
 {
  "test_id": "TEST-CFR-016-2",
  "source_id": "PMS-AFR-134",
  "purpose": "Verify validation of inventor information",
  "preconditions": "Inventor data contains errors (e.g., missing middle name).",
  "action_or_input": "Submit the application with invalid data.",
  "expected_result": "System validates and alerts on incorrect inventor info."
 },
 {
  "test_id": "TEST-CFR-016-3",
  "source_id": "PMS-AFR-135",
  "purpose": "Verify validation of ownership percentages for inventors",
  "preconditions": "Ownership shares sum to less than 100%.",
  "action_or_input": "Save the application record.",
  "expected_result": "System prevents save and requires correct total."
 },
 {
  "test_id": "TEST-CFR-016-4",
  "source_id": "PMS-AFR-136",
  "purpose": "Verify requirement of inventor consent before filing",
  "preconditions": "Inventor agreement is not signed.",
  "action_or_input": "Attempt to file the application.",
  "expected_result": "System blocks filing and requires signed consent."
 },
 {
  "test_id": "TEST-CFR-016-5",
  "source_id": "PMS-AFR-137",
  "purpose": "Verify collection of electronic signatures for inventor consent/agreement (if permitted)",
  "preconditions": "Legal permission for e-signature exists.",
  "action_or_input": "Applicant uploads or signs the agreement electronically.",
  "expected_result": "Electronic signature is collected and recorded."
 },
 {
  "test_id": "TEST-CFR-016-6",
  "source_id": "PMS-AFR-138",
  "purpose": "Verify validation of electronic signatures (if permitted)",
  "preconditions": "Applicant attempts to submit a document with an invalid signature hash.",
  "action_or_input": "Submit the file.",
  "expected_result": "System rejects or flags the invalid signature."
 },
 {
  "test_id": "TEST-CFR-016-7",
  "source_id": "PMS-AFR-140",
  "purpose": "Verify notification to affected parties on inventor information changes",
  "preconditions": "Inventor details are changed.",
  "action_or_input": "Monitor communication logs.",
  "expected_result": "Affected parties (other inventors) receive a notification."
 },
 {
  "test_id": "TEST-CFR-017-0",
  "source_id": "PMS-AFR-141",
  "purpose": "Verify Applicant search of prior-art references",
  "preconditions": "Applicant has access to search tools.",
  "action_or_input": "Applicant initiates a search query.",
  "expected_result": "Search interface is available."
 },
 {
  "test_id": "TEST-CFR-017-1",
  "source_id": "PMS-AFR-142",
  "purpose": "Verify Attorney search of prior-art references",
  "preconditions": "Attorney has access to search tools.",
  "action_or_input": "Attorney initiates a search query.",
  "expected_result": "Search interface is available."
 }
]
```
