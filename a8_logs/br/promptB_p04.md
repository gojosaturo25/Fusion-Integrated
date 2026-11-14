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

The frozen BR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 25 to 32 of 81; write exactly these test cases into tests/a8/br/test_br_p04.py.
```json
[
 {
  "test_id": "BR-PMS-045",
  "source_id": "BR-PMS-045",
  "purpose": "Verify PMS blocks assignment based on applicant preference if preferred attorney is not in panel.",
  "preconditions": "Applicant prefers Attorney X. Attorney X is NOT in the approved panel. System allows preference consideration only if in panel.",
  "action_or_input": "System attempts to assign based solely on Applicant's preference for Attorney X (outside panel).",
  "expected_result": "Assignment blocked or overridden; system ignores preference because preferred attorney is not in the approved panel.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-046",
  "source_id": "BR-PMS-046",
  "purpose": "Verify PMS rejects Attorney opinions with invalid recommendation format.",
  "preconditions": "Attorney creates opinion containing two recommendations (e.g., 'File Patent AND Do Not File') or one not in the list.",
  "action_or_input": "User attempts to finalize and submit the patentability opinion.",
  "expected_result": "Submission rejected; system validates that exactly one recommendation exists from the allowed set.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-048",
  "source_id": "BR-PMS-048",
  "purpose": "Verify PMS includes filing fees in generated budget data.",
  "preconditions": "Budget form initialized for an application with defined expenses.",
  "action_or_input": "User generates or views the Budget report/record.",
  "expected_result": "Report displays 'Filing Fees' as a mandatory line item/component.",
  "test_type": "Unit"
 },
 {
  "test_id": "BR-PMS-049",
  "source_id": "BR-PMS-049",
  "purpose": "Verify PMS includes attorney fees in generated budget data.",
  "preconditions": "Budget form initialized for an application with defined expenses.",
  "action_or_input": "User generates or views the Budget report/record.",
  "expected_result": "Report displays 'Attorney Fees' as a mandatory line item/component.",
  "test_type": "Unit"
 },
 {
  "test_id": "BR-PMS-050",
  "source_id": "BR-PMS-050",
  "purpose": "Verify PMS includes administrative costs in generated budget data.",
  "preconditions": "Budget form initialized for an application with defined expenses.",
  "action_or_input": "User generates or views the Budget report/record.",
  "expected_result": "Report displays 'Administrative Costs' as a mandatory line item/component.",
  "test_type": "Unit"
 },
 {
  "test_id": "BR-PMS-051",
  "source_id": "BR-PMS-051",
  "purpose": "Verify PMS routes/escalates budget exceeding threshold to higher authority.",
  "preconditions": "Total calculated cost is \\$X where X > configured threshold limit. Director proposes approval.",
  "action_or_input": "System processes the approval request for the high-cost budget.",
  "expected_result": "Request routed/escalated to Higher Authority instead of being approved directly by Director.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-052",
  "source_id": "BR-PMS-052",
  "purpose": "Verify PMS blocks Budget approval if application status is not Approved.",
  "preconditions": "Application status is 'Under Review'. Director attempts to approve budget.",
  "action_or_input": "User clicks 'Approve Budget' button.",
  "expected_result": "Action denied; system returns error stating Budget approval allowed only for Approved applications.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-053",
  "source_id": "BR-PMS-053",
  "purpose": "Verify PMS requires budget availability validation when data is available.",
  "preconditions": "System has access to external financial data showing insufficient funds. Director attempts to approve budget.",
  "action_or_input": "User proceeds with budget approval without verifying availability first.",
  "expected_result": "Approval blocked; system forces/validates against available budget data and rejects if unavailable.",
  "test_type": "Acceptance"
 }
]
```
