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

The frozen BR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 9 to 16 of 81; write exactly these test cases into tests/a8/br/test_br_p02.py.
```json
[
 {
  "test_id": "BR-PMS-022",
  "source_id": "BR-PMS-022",
  "purpose": "Verify PMS prevents automatic assignment without configured rules.",
  "preconditions": "PCC_ADMIN attempts to assign an application; Automatic routing mechanism enabled in config but no specific expertise rules defined for a department.",
  "action_or_input": "User initiates 'Auto-Assign' feature.",
  "expected_result": "System rejects the auto-assignment attempt or logs warning indicating lack of governing criteria.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-023",
  "source_id": "BR-PMS-023",
  "purpose": "Verify PMS enforces Director expertise matching during assignment.",
  "preconditions": "Director D has 'Legal' expertise. Application type is 'Software Patent'. User initiates assignment for this application.",
  "action_or_input": "System auto-routes or manual assigns Application to Director D.",
  "expected_result": "Assignment validated against domain; system ensures/flags appropriate matching based on legal domain.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-024",
  "source_id": "BR-PMS-024",
  "purpose": "Verify PMS enforces Director workload balance during assignment.",
  "preconditions": "Director D currently handles max capacity; another director E has free capacity. Application available for review.",
  "action_or_input": "System auto-routes application to Director D.",
  "expected_result": "Assignment blocked or routed automatically to Director E based on workload balance constraint.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-025",
  "source_id": "BR-PMS-025",
  "purpose": "Verify PMS checks conflict-of-interest before Director assignment.",
  "preconditions": "Director D is listed as an inventor on Application X. User attempts to assign Application X to Director D.",
  "action_or_input": "System processes the assignment request.",
  "expected_result": "Assignment rejected; system returns error indicating Conflict of Interest detected (Director is inventor).",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-026",
  "source_id": "BR-PMS-026",
  "purpose": "Verify PMS blocks Director review if they are listed as inventor.",
  "preconditions": "Director D is registered in the system and listed as an inventor on Application X. Application status is 'Under Review'.",
  "action_or_input": "Director D attempts to access the 'Review' function for Application X.",
  "expected_result": "Access denied; Director receives notification of restriction due to being listed as inventor.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-027",
  "source_id": "BR-PMS-027",
  "purpose": "Verify PCC_ADMIN cannot review applications where they are inventors.",
  "preconditions": "PCC_ADMIN is listed as an inventor on Application X.",
  "action_or_input": "PCC_ADMIN attempts to view Application X for review decision purposes.",
  "expected_result": "Access denied; system flags conflict of interest preventing review role.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-029",
  "source_id": "BR-PMS-029",
  "purpose": "Verify PMS rejects Director decisions other than Approve, Reject, Needs Revision.",
  "preconditions": "Director D is reviewing Application X. Decision dropdown/UI element available.",
  "action_or_input": "Director selects 'Withdraw' as the decision option and attempts to save.",
  "expected_result": "Validation fails; system rejects 'Withdraw' and prompts for valid options (Approve, Reject, Needs Revision).",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-030",
  "source_id": "BR-PMS-030",
  "purpose": "Verify PMS rejects Director decision with justification < 50 characters.",
  "preconditions": "Director D selects 'Approve' and enters justification text consisting of exactly 49 characters.",
  "action_or_input": "User attempts to submit/save the review decision.",
  "expected_result": "Submission blocked; system returns error indicating minimum 50 character justification required.",
  "test_type": "Acceptance"
 }
]
```
