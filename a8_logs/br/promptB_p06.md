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

The frozen BR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 41 to 48 of 81; write exactly these test cases into tests/a8/br/test_br_p06.py.
```json
[
 {
  "test_id": "BR-PMS-068",
  "source_id": "BR-PMS-068",
  "purpose": "Verify PMS validates withdrawal eligibility against specific status rules.",
  "preconditions": "Application status is 'Rejected'. User attempts to withdraw.",
  "action_or_input": "User initiates withdrawal process.",
  "expected_result": "System checks current status configuration; withdrawal permitted/disallowed based on 'withdrawal-eligible' rule for Rejected status.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-069",
  "source_id": "BR-PMS-069",
  "purpose": "Verify PMS requires a reason for withdrawal requests.",
  "preconditions": "Withdrawal form open.",
  "action_or_input": "User attempts to submit the withdrawal without providing a reason text field.",
  "expected_result": "Submission blocked; system requires Applicant-provided reason input.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-070",
  "source_id": "BR-PMS-070",
  "purpose": "Verify PMS records co-inventor consent when process requires it.",
  "preconditions": "Application has multiple inventors. Process rules configured to require consent for withdrawal.",
  "action_or_input": "Applicant attempts to withdraw application.",
  "expected_result": "System prompts for or validates recording of Co-inventor consent before proceeding.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-073",
  "source_id": "BR-PMS-073",
  "purpose": "Verify PMS validates inventor information before acceptance.",
  "preconditions": "Inventor details (name, email) incomplete or invalid format.",
  "action_or_input": "User attempts to save/update inventor information.",
  "expected_result": "Update rejected; system returns validation error for inventor information.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-074",
  "source_id": "BR-PMS-074",
  "purpose": "Verify PMS validates ownership percentages before acceptance.",
  "preconditions": "Ownership percentage sum > 100% or negative value entered.",
  "action_or_input": "User attempts to save/update ownership share data.",
  "expected_result": "Update rejected; system returns validation error for ownership percentages.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-075",
  "source_id": "BR-PMS-075",
  "purpose": "Verify PMS enforces inventor consent requirement before filing.",
  "preconditions": "Filing stage approaching; Consent status 'Pending'.",
  "action_or_input": "System attempts to proceed to External Filing stage.",
  "expected_result": "Filing blocked; system waits for Required inventor consent to be obtained/completed.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-076",
  "source_id": "BR-PMS-076",
  "purpose": "Verify PMS restricts electronic signature collection where not legally permitted.",
  "preconditions": "System configuration indicates 'Electronic Signatures' disabled for region X. User (Attorney) attempts to collect e-sig from applicant in region X.",
  "action_or_input": "User selects 'Collect Electronic Signature' and clicks confirm.",
  "expected_result": "Action blocked; system prevents e-signature collection unless legally permitted and configured.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-077",
  "source_id": "BR-PMS-077",
  "purpose": "Verify PMS only validates e-signatures where permitted and configured.",
  "preconditions": "E-sig data submitted; Legal configuration enabled for this jurisdiction.",
  "action_or_input": "User attempts to submit/validate the electronic signature record.",
  "expected_result": "Validation performed only if legally permitted and configured is true; otherwise rejected/not validated.",
  "test_type": "Acceptance"
 }
]
```
