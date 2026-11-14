You are given:
1. the frozen A8_BASE Fusion implementation, and
2. the frozen BR_DESIGN.json.
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
- Store generated tests only under tests/a8/br/.
If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.

The frozen BR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 65 to 72 of 81; write exactly these test cases into tests/a8/br/test_br_p09.py.
```json
[
 {
  "test_id": "BR-PMS-102",
  "source_id": "BR-PMS-102",
  "purpose": "Verify PMS generates 15-day deadline alerts where applicable.",
  "preconditions": "Deadline event set for T. Current time is T - 20 days. Alert config enabled for '15 day'.",
  "action_or_input": "System checks trigger conditions for notifications.",
  "expected_result": "Alert generated and sent to relevant stakeholders.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-103",
  "source_id": "BR-PMS-103",
  "purpose": "Verify PMS generates 5-day deadline alerts where applicable.",
  "preconditions": "Deadline event set for T. Current time is T - 7 days. Alert config enabled for '5 day'.",
  "action_or_input": "System checks trigger conditions for notifications.",
  "expected_result": "Alert generated and sent to relevant stakeholders.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-104",
  "source_id": "BR-PMS-104",
  "purpose": "Verify PMS escalates missed deadlines according to chain.",
  "preconditions": "Missed deadline event (e.g., 5-day alert ignored). Escalation chain configured.",
  "action_or_input": "System processes 'Missed Deadline' status.",
  "expected_result": "Escalation triggered and routed according to the configured escalation chain.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-116",
  "source_id": "BR-PMS-116",
  "purpose": "Verify PMS scope limits email triggering to system generation.",
  "preconditions": "User logged in. Notification payload ready (e.g., Application Approved).",
  "action_or_input": "System attempts to execute full email delivery including subject, body, and SMTP sending.",
  "expected_result": "PMS triggers the creation of the notification object/email draft but does not control/deliver external infrastructure; logs show PMS trigger only.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-121",
  "source_id": "BR-PMS-121",
  "purpose": "Verify audit logs include specific fields for applicable actions.",
  "preconditions": "User A performs 'Delete Document' action. Audit log creation enabled.",
  "action_or_input": "System generates the audit record immediately after action completion.",
  "expected_result": "Record includes: User ID, Action Type, Timestamp, Application ID, Previous State, New State.",
  "test_type": "Unit"
 },
 {
  "test_id": "BR-PMS-122",
  "source_id": "BR-PMS-122",
  "purpose": "Verify PMS creates immutable audit records for critical operations.",
  "preconditions": "User performs 'Delete Application' (Critical). Audit logging enabled.",
  "action_or_input": "System commits the action to the database.",
  "expected_result": "Audit record created and marked as 'Immutable' (writable only by system, no user edit capability).",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-126",
  "source_id": "BR-PMS-126",
  "purpose": "Verify PMS blocks access without valid role assignment.",
  "preconditions": "User account exists but has 'Guest' or no assigned role. Attempt to access Patent Management function.",
  "action_or_input": "User logs in and navigates to a protected module/page.",
  "expected_result": "Access denied; system redirects/error states user needs a valid PMS role assignment.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-127",
  "source_id": "BR-PMS-127",
  "purpose": "Verify PMS prevents Attorney assignment before Director approval.",
  "preconditions": "Application status 'Under Review' (no Director Approval). PCC_ADMIN attempts to assign Attorney.",
  "action_or_input": "User initiates 'Assign Attorney' workflow.",
  "expected_result": "Action denied; system error states Attorney assignment must wait for recorded Director approval.",
  "test_type": "Acceptance"
 }
]
```
