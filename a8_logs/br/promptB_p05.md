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

The frozen BR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 33 to 40 of 81; write exactly these test cases into tests/a8/br/test_br_p05.py.
```json
[
 {
  "test_id": "BR-PMS-055",
  "source_id": "BR-PMS-055",
  "purpose": "Verify PMS validates filing package format against standards where rules are available.",
  "preconditions": "PMS has configured validation rules for Patent Office format. Attorney prepares and submits filing package.",
  "action_or_input": "System performs format validation check on the package.",
  "expected_result": "Recorded readiness status is set only if package satisfies applicable patent-office format standards.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-056",
  "source_id": "BR-PMS-056",
  "purpose": "Verify PMS enforces recording of additional justification for international filings.",
  "preconditions": "Attorney attempts to file application as 'International' type without justification field populated.",
  "action_or_input": "User submits the International filing action.",
  "expected_result": "Action blocked or requires entry of 'additional justification' before submission is allowed.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-059",
  "source_id": "BR-PMS-059",
  "purpose": "Verify PMS activates post-grant tracking only upon Granted status.",
  "preconditions": "Application status is 'Under Review'. Post-grant features (reminders, fee calc) attempted to be viewed/used.",
  "action_or_input": "User attempts to access 'Maintenance Fee Calculator' or similar post-grant tool.",
  "expected_result": "Feature unavailable; system returns error stating tracking activated only for Granted status.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-060",
  "source_id": "BR-PMS-060",
  "purpose": "Verify PMS calculates maintenance schedule based on grant date/jurisdiction.",
  "preconditions": "Patent Granted. Jurisdiction 'US' set. Grant Date set to T0.",
  "action_or_input": "System calculates/retreives maintenance-fee schedule record.",
  "expected_result": "Schedule generated/calculated correctly based on the specific grant date and jurisdiction parameters provided.",
  "test_type": "Unit"
 },
 {
  "test_id": "BR-PMS-061",
  "source_id": "BR-PMS-061",
  "purpose": "Verify PMS requires explicit Renew or Do Not Renew decision before each maintenance deadline.",
  "preconditions": "Maintenance Deadline approaching. System pending decision state.",
  "action_or_input": "Attempt to close the maintenance tracking loop without making a Renew/DoNotRenew choice.",
  "expected_result": "System blocks progress; error indicates explicit Renew or Do Not Renew decision is required.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-065",
  "source_id": "BR-PMS-065",
  "purpose": "Verify PMS enforces deadline compliance for Office Action responses.",
  "preconditions": "Office action received; Deadline D passed. Response not submitted by attorney.",
  "action_or_input": "System evaluates submission status at T > D.",
  "expected_result": "Response marked as 'Missed' or error indicating non-compliance unless extension was recorded.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-066",
  "source_id": "BR-PMS-066",
  "purpose": "Verify PMS automates deadline tracking only where rules are available.",
  "preconditions": "Office action received; Applicable jurisdiction has no configured deadline data/rules in system.",
  "action_or_input": "System attempts to generate automatic deadline alerts or monitoring logs for this case.",
  "expected_result": "Alerts not generated; manual tracking mode enforced or system states 'No deadline rule available'.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-067",
  "source_id": "BR-PMS-067",
  "purpose": "Verify PMS restricts withdrawal to pre-filing stage.",
  "preconditions": "Application status is 'Filed' or 'Under Review'. Applicant attempts to withdraw.",
  "action_or_input": "User selects 'Withdraw Application' button.",
  "expected_result": "Action denied; system returns error stating withdrawal allowed only before filing stage.",
  "test_type": "Acceptance"
 }
]
```
