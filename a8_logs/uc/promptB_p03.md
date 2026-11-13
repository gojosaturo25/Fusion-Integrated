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

The frozen UC_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 17 to 24 of 39; write exactly these test cases into tests/a8/uc/test_uc_p03.py.
```json
[
 {
  "test_id": "TEST-PMS-UC008-MIN",
  "source_id": "UC-PMS-008 Exception Flows (No Justification)",
  "purpose": "Verify that review decisions without sufficient justification are rejected.",
  "preconditions": "Director attempts to submit a decision with fewer than 50 characters of justification.",
  "action_or_input": "Director submits the incomplete decision.",
  "expected_result": "PMS rejects the decision; no business state changes occur."
 },
 {
  "test_id": "TEST-PMS-UC010-MAX",
  "source_id": "UC-PMS-010 Main Success Scenario",
  "purpose": "Verify that approved applications can be assigned attorneys from the approved panel.",
  "preconditions": "Application status is Approved; PCC_ADMIN is authorized.",
  "action_or_input": "PCC_ADMIN selects an attorney from the approved panel (considering preference/conflict).",
  "expected_result": "PMS records the assignment, notifies the Attorney for acceptance/decline, and updates status to Attorney Assigned/Pending Review."
 },
 {
  "test_id": "TEST-PMS-010-MIN",
  "source_id": "UC-PMS-010 Exception Flows (Non-Panel)",
  "purpose": "Verify that non-panel attorneys are only assigned if an institutional exception exists.",
  "preconditions": "PCC_ADMIN attempts to assign an attorney not in the approved panel without a recorded exception.",
  "action_or_input": "PCC_ADMIN selects the non-panel attorney.",
  "expected_result": "PMS blocks assignment unless a valid institutional exception is recorded/allowed."
 },
 {
  "test_id": "TEST-PMS-UC011-MAX",
  "source_id": "UC-PMS-011 Main Success Scenario",
  "purpose": "Verify that Attorneys can accept or decline assignments.",
  "preconditions": "An assignment to the Attorney exists and is active.",
  "action_or_input": "Attorney selects Accept or Decline for the assignment.",
  "expected_result": "PMS records response. Acceptance updates status to Attorney Assigned; Decline updates to Pending Review and notifies PCC_ADMIN."
 },
 {
  "test_id": "TEST-PMS-UC012-MAX",
  "source_id": "UC-PMS-012 Main Success Scenario",
  "purpose": "Verify that Attorneys record patentability opinions with valid recommendations.",
  "preconditions": "Attorney has an assigned application and access to review details.",
  "action_or_input": "Attorney conducts assessment and selects one recommendation: File Patent, Do Not File, or Needs Amendment.",
  "expected_result": "PMS records the opinion/recommendation and notifies stakeholders."
 },
 {
  "test_id": "TEST-PMS-UC013-MAX",
  "source_id": "UC-PMS-013 Main Success Scenario",
  "purpose": "Verify that Attorneys can prepare, validate, and record external patent filings.",
  "preconditions": "Required approvals, budget allocation, and inventor agreements are complete; Attorney has filing authority.",
  "action_or_input": "Attorney prepares package, performs validation (if available), submits externally, and records confirmation details.",
  "expected_result": "PMS sets application status to Filed, records audit/history, and triggers confirmation notification."
 },
 {
  "test_id": "TEST-PMS-UC013-MIN",
  "source_id": "UC-PMS-013 Exception Flows (Prerequisites)",
  "purpose": "Verify that external filing is blocked if prerequisite approvals or agreements are missing.",
  "preconditions": "Required budget approval or inventor agreement is missing for the application.",
  "action_or_input": "Attorney attempts to submit the filing package.",
  "expected_result": "PMS blocks the filing action."
 },
 {
  "test_id": "TEST-PMS-UC015-MAX",
  "source_id": "UC-PMS-015 Main Success Scenario",
  "purpose": "Verify that Attorneys can submit office-action responses, handling optional Applicant review.",
  "preconditions": "Office action exists; Attorney has access; applicable deadline/extension data is available.",
  "action_or_input": "Attorney prepares response (optional: records Applicant approval) and submits the response externally.",
  "expected_result": "PMS updates response tracking, audit/history, and maintains status. Extension requests are recorded if allowed."
 }
]
```
