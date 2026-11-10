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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 73 to 80 of 204; write exactly these test cases into tests/a8/fr/test_fr_p10.py.
```json
[
 {
  "test_id": "TEST-CFR-012-4",
  "source_id": "PMS-AFR-103",
  "purpose": "Verify requirement of additional justification for international filings",
  "preconditions": "Application is being filed internationally.",
  "action_or_input": "Proceed with filing without justification.",
  "expected_result": "The system blocks the action and requires justification."
 },
 {
  "test_id": "TEST-CFR-012-5",
  "source_id": "PMS-AFR-104",
  "purpose": "Verify capture of filing ID, date, and confirmation",
  "preconditions": "Filing is recorded.",
  "action_or_input": "View the application's filing metadata.",
  "expected_result": "External Filing ID, Date, and Confirmation info are visible."
 },
 {
  "test_id": "TEST-CFR-012-6",
  "source_id": "PMS-AFR-105",
  "purpose": "Verify status update to 'Filed'",
  "preconditions": "Filing is recorded.",
  "action_or_input": "Check application status.",
  "expected_result": "Status updates from 'Attorney Assigned' to 'Filed'."
 },
 {
  "test_id": "TEST-CFR-012-7",
  "source_id": "PMS-AFR-106",
  "purpose": "Verify logging of official patent office communications",
  "preconditions": "A response or notification is received from the Patent Office.",
  "action_or_input": "Access the communication log.",
  "expected_result": "Official communications are logged."
 },
 {
  "test_id": "TEST-CFR-013-0",
  "source_id": "PMS-AFR-107",
  "purpose": "Verify activation of post-grant tracking only for 'Granted' status",
  "preconditions": "Application status is 'Under Review'.",
  "action_or_input": "Check the Post-Grant Maintenance menu.",
  "expected_result": "The menu is unavailable or not applicable."
 },
 {
  "test_id": "TEST-CFR-013-1",
  "source_id": "PMS-AFR-107-alt",
  "purpose": "Verify activation of post-grant tracking for 'Granted' status",
  "preconditions": "Application status is 'Granted'.",
  "action_or_input": "Check the Post-Grant Maintenance menu.",
  "expected_result": "The maintenance tracking interface becomes available."
 },
 {
  "test_id": "TEST-CFR-013-2",
  "source_id": "PMS-AFR-108",
  "purpose": "Verify calculation of maintenance-fee schedules from grant date",
  "preconditions": "Application is 'Granted'.",
  "action_or_input": "View the Maintenance Schedule.",
  "expected_result": "Fees and deadlines are calculated based on the grant date."
 },
 {
  "test_id": "TEST-CFR-013-3",
  "source_id": "PMS-AFR-109",
  "purpose": "Verify Attorney management of maintenance reminders/deadlines",
  "preconditions": "Application is 'Granted' and approaching a deadline.",
  "action_or_input": "Attorney views the dashboard.",
  "expected_result": "Reminders and deadlines for maintenance fees are displayed."
 }
]
```
