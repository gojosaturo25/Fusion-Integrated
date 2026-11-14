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

The frozen BR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 57 to 64 of 81; write exactly these test cases into tests/a8/br/test_br_p08.py.
```json
[
 {
  "test_id": "BR-PMS-093",
  "source_id": "BR-PMS-093",
  "purpose": "Verify PMS enforces appeal filing deadline.",
  "preconditions": "Rejection date set. Current time > configured appeal deadline period.",
  "action_or_input": "User attempts to submit appeal form.",
  "expected_result": "Action blocked; system returns error stating appeal must be filed within allowed period.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-094",
  "source_id": "BR-PMS-094",
  "purpose": "Verify PMS validates grounds and justification in appeal submissions.",
  "preconditions": "Appeal form open. Justification text field empty or insufficient.",
  "action_or_input": "User attempts to submit the Appeal request.",
  "expected_result": "Submission blocked; system requires Applicant-provided grounds and justification.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-095",
  "source_id": "BR-PMS-095",
  "purpose": "Verify PMS rejects Director appeal outcomes other than Uphold, Remand, Modify.",
  "preconditions": "Director reviewing Appeal X. Decision dropdown/UI available.",
  "action_or_input": "Director selects 'Overturn' (unsupported option) as the outcome.",
  "expected_result": "Validation fails; system rejects invalid options and prompts for valid ones (Uphold, Remand, Modify).",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-097",
  "source_id": "BR-PMS-097",
  "purpose": "Verify PMS calculates Director review deadline.",
  "preconditions": "Application assigned to Director. System initialized.",
  "action_or_input": "System executes 'Calculate Deadline' logic.",
  "expected_result": "System generates alert/calendar entry for the Director review deadline based on applicable rule.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-098",
  "source_id": "BR-PMS-098",
  "purpose": "Verify PMS calculates revision deadline.",
  "preconditions": "Revision decision made. System initialized.",
  "action_or_input": "System executes 'Calculate Deadline' logic for the revision period.",
  "expected_result": "System generates alert/calendar entry based on applicable revision-deadline rule (e.g., 60 days).",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-099",
  "source_id": "BR-PMS-099",
  "purpose": "Verify PMS calculates office-action deadlines only where rules are available.",
  "preconditions": "Office action received; No jurisdictional deadline data configured for this case.",
  "action_or_input": "System attempts to set up automated deadline tracking/alerts.",
  "expected_result": "Tracking disabled/not automated; system indicates lack of applicable deadline rule/data.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-100",
  "source_id": "BR-PMS-100",
  "purpose": "Verify PMS calculates maintenance deadlines only where rules are available.",
  "preconditions": "Patent Granted; No jurisdictional schedule data configured in system.",
  "action_or_input": "System attempts to set up automated deadline tracking/alerts for fees.",
  "expected_result": "Tracking disabled/not automated; system indicates lack of applicable schedule rule/data.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-101",
  "source_id": "BR-PMS-101",
  "purpose": "Verify PMS generates 30-day deadline alerts where applicable.",
  "preconditions": "Deadly event set for T. Current time is T - 25 days. Alert config enabled for '30 day'.",
  "action_or_input": "System checks trigger conditions for notifications.",
  "expected_result": "Alert generated and sent to relevant stakeholders.",
  "test_type": "Acceptance"
 }
]
```
