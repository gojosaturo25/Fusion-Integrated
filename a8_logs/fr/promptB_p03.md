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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 17 to 24 of 204; write exactly these test cases into tests/a8/fr/test_fr_p03.py.
```json
[
 {
  "test_id": "TEST-CFR-005-8",
  "source_id": "PMS-AFR-046",
  "purpose": "Verify enforcement of inventor agreement prerequisite",
  "preconditions": "An application is submitted without completed inventor agreements.",
  "action_or_input": "Attempt to proceed with submission processing.",
  "expected_result": "The system blocks submission and displays an error indicating inventor agreements are incomplete."
 },
 {
  "test_id": "TEST-CFR-005-9",
  "source_id": "PMS-AFR-047",
  "purpose": "Verify application history recording",
  "preconditions": "Application status is 'Submitted'.",
  "action_or_input": "Navigate to the application details page.",
  "expected_result": "A history log showing submission event, timestamp, and user is visible."
 },
 {
  "test_id": "TEST-CFR-005-10",
  "source_id": "PMS-AFR-048",
  "purpose": "Verify stakeholder notification on submission",
  "preconditions": "Application submission is successful.",
  "action_or_input": "Monitor the system notification log for Applicant and Stakeholders.",
  "expected_result": "A notification is generated confirming application submission."
 },
 {
  "test_id": "TEST-CFR-006-0",
  "source_id": "PMS-AFR-049",
  "purpose": "Verify manual assignment of Director by PCC_ADMIN",
  "preconditions": "An application exists with status 'Submitted'.",
  "action_or_input": "PCC_ADMIN navigates to 'Assign Applications' and selects a Director.",
  "expected_result": "The application is assigned to the selected Director and workflow updates."
 },
 {
  "test_id": "TEST-CFR-006-1",
  "source_id": "PMS-AFR-050",
  "purpose": "Verify automatic assignment based on rules",
  "preconditions": "An application exists with status 'Submitted' and assignment rules are configured.",
  "action_or_input": "Navigate to 'Submit Applications'.",
  "expected_result": "The system automatically assigns the application without manual intervention."
 },
 {
  "test_id": "TEST-CFR-006-2",
  "source_id": "PMS-AFR-051",
  "purpose": "Verify assignment based on Director expertise matching",
  "preconditions": "Application domain is 'Chemistry'. Director A has 'Biology' expertise; Director B has 'Chemistry' expertise.",
  "action_or_input": "Initiate application processing.",
  "expected_result": "The system selects the Director with matching 'Chemistry' expertise."
 },
 {
  "test_id": "TEST-CFR-006-3",
  "source_id": "PMS-AFR-052",
  "purpose": "Verify assignment based on workload balance",
  "preconditions": "Two eligible Directors exist; Director A has heavy load, Director B has light load.",
  "action_or_input": "Initiate application processing.",
  "expected_result": "The system assigns the application to Director B to maintain balance."
 },
 {
  "test_id": "TEST-CFR-006-4",
  "source_id": "PMS-AFR-053",
  "purpose": "Verify conflict-of-interest check before assignment",
  "preconditions": "The Director being assigned is listed as an inventor on the application.",
  "action_or_input": "Attempt to assign the application to this Director via the admin interface.",
  "expected_result": "The system blocks the assignment and flags a Conflict of Interest."
 }
]
```
