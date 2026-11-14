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

The frozen BR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 17 to 24 of 81; write exactly these test cases into tests/a8/br/test_br_p03.py.
```json
[
 {
  "test_id": "BR-PMS-031",
  "source_id": "BR-PMS-031",
  "purpose": "Verify PMS enforces Director review deadline of 15 business days.",
  "preconditions": "Director D assigned to Application X; Current time is T0. Deadline for completion is T1 (15 business days later).",
  "action_or_input": "System checks status at T2 where T2 > T1 without completed review.",
  "expected_result": "System flags overdue; alerts generated or workflow stalled pending handling of the deadline violation.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-033",
  "source_id": "BR-PMS-033",
  "purpose": "Verify PMS blocks revision submission if status is not Needs Revision or Rejected.",
  "preconditions": "Application status is 'Approved'. User attempts to initiate 'Revision' action.",
  "action_or_input": "User clicks 'Revise Application' button in Approved application view.",
  "expected_result": "Action blocked; system returns error stating revision is not permitted for current status.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-034",
  "source_id": "BR-PMS-034",
  "purpose": "Verify PMS allows revision submission if status is Rejected.",
  "preconditions": "Application status is 'Rejected'. User attempts to initiate 'Revision' action.",
  "action_or_input": "User clicks 'Revise Application' button in Rejected application view.",
  "expected_result": "Action permitted; user can proceed with revision upload/submission.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-035",
  "source_id": "BR-PMS-035",
  "purpose": "Verify PMS monitors and validates 60-day resubmission deadline.",
  "preconditions": "Rejection/Revision decision made on Date D. Current time is D + 61 days.",
  "action_or_input": "System attempts to calculate eligibility for new submission without having been revised.",
  "expected_result": "Eligibility check returns 'Expired' or system changes application status to Expired automatically.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-036",
  "source_id": "BR-PMS-036",
  "purpose": "Verify PMS rejects revision submissions that do not address Director feedback.",
  "preconditions": "Application has specific feedback text. User submits new documents claiming to be a revision but omitting references to the feedback.",
  "action_or_input": "User attempts to resubmit application as a valid revision.",
  "expected_result": "Submission rejected; system returns error stating revision must address recorded Director feedback.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-038",
  "source_id": "BR-PMS-038",
  "purpose": "Verify PMS updates status to Expired after deadline expiration.",
  "preconditions": "Application in Revision cycle. 60 day period expired. No valid resubmission made.",
  "action_or_input": "System executes 'Process Expiry' logic.",
  "expected_result": "Application status changes from 'Needs Revision' or 'Rejected' to 'Expired'.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-040",
  "source_id": "BR-PMS-040",
  "purpose": "Verify PMS restricts Attorney assignment role to PCC_ADMIN only.",
  "preconditions": "Director D has approved the application. User logged in as Director (not PCC_ADMIN).",
  "action_or_input": "Director attempts to select and assign an attorney to the application.",
  "expected_result": "Action denied; system returns error stating only PCC_ADMIN can assign attorneys.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-041",
  "source_id": "BR-PMS-041",
  "purpose": "Verify PMS enforces selection from approved panel unless exception recorded.",
  "preconditions": "Attorney O is NOT in the approved panel. User (PCC_ADMIN) attempts to assign Attorney O.",
  "action_or_input": "User selects Attorney O for assignment without creating an institutional exception record first.",
  "expected_result": "Assignment blocked; system returns error stating attorney not on approved panel or requires exception.",
  "test_type": "Acceptance"
 }
]
```
