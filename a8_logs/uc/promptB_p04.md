You are given:
1. the frozen A8_BASE Fusion implementation, and
2. the frozen UC_DESIGN.json.
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
- Store generated tests only under tests/a8/uc/.
If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.

The frozen UC_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 25 to 32 of 39; write exactly these test cases into tests/a8/uc/test_uc_p04.py.
```json
[
 {
  "test_id": "TEST-PMS-UC015-MIN",
  "source_id": "UC-PMS-015 Exception Flows (Approval)",
  "purpose": "Verify that responses cannot be marked submitted without required Applicant approval (when applicable).",
  "preconditions": "Process requires Applicant review; draft is available but not yet approved.",
  "action_or_input": "Attorney attempts to finalize and submit the response without Applicant approval.",
  "expected_result": "PMS does not mark the response as submitted; response status remains awaiting approval."
 },
 {
  "test_id": "TEST-PMS-UC016-MAX",
  "source_id": "UC-PMS-016 Main Success Scenario",
  "purpose": "Verify that PCC_ADMIN can monitor deadlines and handle escalations.",
  "preconditions": "Active authorized role; deadline records exist or are calculable.",
  "action_or_input": "PCC_ADMIN views monitoring view, reviews alerts (30/15/5 days), and handles missed deadline escalations.",
  "expected_result": "PMS calculates/maintains deadlines, generates alerts, logs activity, and routes/escalates delayed cases."
 },
 {
  "test_id": "TEST-PMS-UC017-MAX",
  "source_id": "UC-PMS-017 Main Success Scenario",
  "purpose": "Verify that post-grant tracking activates and renewal decisions are recorded.",
  "preconditions": "Patent status is Granted; maintenance deadline approaches.",
  "action_or_input": "Attorney requests a Renewal decision from the Director.",
  "expected_result": "Director records Renew or Do Not Renew; if Renewed, Attorney processes action and PMS updates status/history."
 },
 {
  "test_id": "TEST-PMS-UC018-MAX",
  "source_id": "UC-PMS-018 Main Success Scenario",
  "purpose": "Verify that Directors can record Renewal or Do Not Renew decisions.",
  "preconditions": "Patent is in post-grant tracking; renewal decision is due.",
  "action_or_input": "Director selects Renew or Do Not Renew.",
  "expected_result": "PMS records the decision and makes it available for the Attorney's next action."
 },
 {
  "test_id": "TEST-PMS-UC019-MAX",
  "source_id": "UC-PMS-019 Main Success Scenario",
  "purpose": "Verify that authorized users can upload document versions.",
  "preconditions": "User has valid role; action is permitted for role/status (e.g., Applicant in Needs Revision).",
  "action_or_input": "User uploads a new document version.",
  "expected_result": "PMS assigns next version number, archives previous version, logs modification with user/timestamp."
 },
 {
  "test_id": "TEST-PMS-UC019-MIN",
  "source_id": "UC-PMS-019 Exception Flows (Unauthorized)",
  "purpose": "Verify that unauthorized users cannot upload document versions.",
  "preconditions": "User lacks role or status permission to upload documents.",
  "action_or_input": "User attempts to upload a new document version.",
  "expected_result": "Upload is blocked; prior version history remains consistent."
 },
 {
  "test_id": "TEST-PMS-UC022-MAX",
  "source_id": "UC-PMS-022 Main Success Scenario",
  "purpose": "Verify that Applicants can file appeals within the allowed period.",
  "preconditions": "Application is Rejected; appeal period has not expired.",
  "action_or_input": "Applicant enters grounds/justification and submits the appeal.",
  "expected_result": "PMS validates eligibility/timing, records the appeal for Director review."
 },
 {
  "test_id": "TEST-PMS-UC023-MAX",
  "source_id": "UC-PMS-023 Main Success Scenario",
  "purpose": "Verify that Directors can record specific appeal outcomes.",
  "preconditions": "Appeal exists and is available for review.",
  "action_or_input": "Director selects one outcome: Uphold Rejection, Remand for Amendment, or Modify Decision.",
  "expected_result": "PMS records the outcome and initiates the next applicable process step."
 }
]
```
