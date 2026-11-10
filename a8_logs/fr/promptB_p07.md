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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 49 to 56 of 204; write exactly these test cases into tests/a8/fr/test_fr_p07.py.
```json
[
 {
  "test_id": "TEST-CFR-009-5",
  "source_id": "PMS-AFR-079",
  "purpose": "Verify consideration of Applicant preference (only if approved)",
  "preconditions": "Applicant's preferred Attorney is NOT on the approved panel.",
  "action_or_input": "Submit application for attorney assignment with preference set.",
  "expected_result": "The system does not select the preferred attorney but selects based on other criteria."
 },
 {
  "test_id": "TEST-CFR-009-6",
  "source_id": "PMS-AFR-080",
  "purpose": "Verify requirement of Attorney acceptance/decline",
  "preconditions": "An application is assigned to an attorney.",
  "action_or_input": "Review the status of the assignment record.",
  "expected_result": "The system records the outcome only after the Attorney has accepted or declined."
 },
 {
  "test_id": "TEST-CFR-009-7",
  "source_id": "PMS-AFR-081",
  "purpose": "Verify recording of attorney assignment outcome",
  "preconditions": "Attorney accepts an assignment.",
  "action_or_input": "Check the application status record.",
  "expected_result": "The application status updates to 'Attorney Assigned' (or similar)."
 },
 {
  "test_id": "TEST-CFR-010-0",
  "source_id": "PMS-AFR-082",
  "purpose": "Verify recording of legal and patentability analysis",
  "preconditions": "Attorney has access to the application.",
  "action_or_input": "Attorney enters a detailed patentability analysis report.",
  "expected_result": "The analysis is recorded in the attorney's case file."
 },
 {
  "test_id": "TEST-CFR-010-1",
  "source_id": "PMS-AFR-083",
  "purpose": "Verify recording of prior-art searches",
  "preconditions": "Attorney has access to search tools.",
  "action_or_input": "Conduct a search in the integrated prior-art database.",
  "expected_result": "Search results and details are recorded in the case file."
 },
 {
  "test_id": "TEST-CFR-010-2",
  "source_id": "PMS-AFR-084",
  "purpose": "Verify recording of novelty/non-obviousness/utility evaluation",
  "preconditions": "Attorney has access to the application.",
  "action_or_input": "Input evaluations for Novelty, Non-Obviousness, and Utility.",
  "expected_result": "The three specific evaluations are recorded."
 },
 {
  "test_id": "TEST-CFR-010-3",
  "source_id": "PMS-AFR-085",
  "purpose": "Verify valid patentability recommendation (File/Do Not File/Amend)",
  "preconditions": "Attorney has performed analysis.",
  "action_or_input": "Select a recommendation from the dropdown.",
  "expected_result": "Only 'File Patent', 'Do Not File', or 'Needs Amendment' are allowed."
 },
 {
  "test_id": "TEST-CFR-010-4",
  "source_id": "PMS-AFR-086",
  "purpose": "Verify attorney request for additional information",
  "preconditions": "Attorney is reviewing an application.",
  "action_or_input": "Click 'Request Additional Information' button.",
  "expected_result": "A form appears requesting specific details from the relevant stakeholder."
 }
]
```
