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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 57 to 64 of 204; write exactly these test cases into tests/a8/fr/test_fr_p08.py.
```json
[
 {
  "test_id": "TEST-CFR-010-5",
  "source_id": "PMS-AFR-087",
  "purpose": "Verify attorney request for extensions",
  "preconditions": "Attorney is under time pressure.",
  "action_or_input": "Click 'Request Extension' button.",
  "expected_result": "An extension request form is displayed."
 },
 {
  "test_id": "TEST-CFR-010-6",
  "source_id": "PMS-AFR-088",
  "purpose": "Verify recording of final patentability opinion",
  "preconditions": "Attorney has completed the review.",
  "action_or_input": "Submit the final opinion with recommendation.",
  "expected_result": "The system stores the complete opinion record."
 },
 {
  "test_id": "TEST-CFR-010-7",
  "source_id": "PMS-AFR-089",
  "purpose": "Verify stakeholder notification on attorney opinion",
  "preconditions": "Patentability opinion is recorded.",
  "action_or_input": "Monitor system notifications.",
  "expected_result": "Stakeholders receive a notification regarding the recorded opinion."
 },
 {
  "test_id": "TEST-CFR-011-0",
  "source_id": "PMS-AFR-090",
  "purpose": "Verify Director review of filing/prosecution costs",
  "preconditions": "An application is 'Attorney Assigned' or similar.",
  "action_or_input": "Director views the cost breakdown screen.",
  "expected_result": "Filing fees, attorney fees, and administrative costs are displayed."
 },
 {
  "test_id": "TEST-CFR-011-1",
  "source_id": "PMS-AFR-091",
  "purpose": "Verify Director approval of budget costs",
  "preconditions": "Budget is within limits and available.",
  "action_or_input": "Director clicks 'Approve Budget'.",
  "expected_result": "The budget is approved and recorded."
 },
 {
  "test_id": "TEST-CFR-011-2",
  "source_id": "PMS-AFR-092",
  "purpose": "Verify inclusion of filing fees in budget info",
  "preconditions": "Attorney submits a fee estimate.",
  "action_or_input": "View the detailed budget report.",
  "expected_result": "Filing fees are listed as a distinct line item."
 },
 {
  "test_id": "TEST-CFR-011-3",
  "source_id": "PMS-AFR-093",
  "purpose": "Verify inclusion of attorney fees in budget info",
  "preconditions": "Attorney submits a fee estimate.",
  "action_or_input": "View the detailed budget report.",
  "expected_result": "Attorney fees are listed as a distinct line item."
 },
 {
  "test_id": "TEST-CFR-011-4",
  "source_id": "PMS-AFR-094",
  "purpose": "Verify inclusion of administrative costs in budget info",
  "preconditions": "Admin services are requested.",
  "action_or_input": "View the detailed budget report.",
  "expected_result": "Administrative costs are listed as a distinct line item."
 }
]
```
