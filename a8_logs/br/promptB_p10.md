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

The frozen BR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 73 to 80 of 81; write exactly these test cases into tests/a8/br/test_br_p10.py.
```json
[
 {
  "test_id": "BR-PMS-128",
  "source_id": "BR-PMS-128",
  "purpose": "Verify PMS prevents external filing before approvals and budget are complete.",
  "preconditions": "Application has Approval but Budget is 'Pending'. Attorney attempts External Filing.",
  "action_or_input": "User initiates 'External Filing' action.",
  "expected_result": "Action denied; system error states External filing requires completion of required approvals and budget allocation.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-130",
  "source_id": "BR-PMS-130",
  "purpose": "Verify PMS protects confidential patent info via RBAC.",
  "preconditions": "User has Role 'Guest'. Attempt to view 'Patent Portfolio Report' containing sensitive data.",
  "action_or_input": "System attempts to grant access to the report.",
  "expected_result": "Access denied; system enforces role-based access control restricting confidential info visibility.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-131",
  "source_id": "BR-PMS-131",
  "purpose": "Verify PMS maintains exactly one active PCC_ADMIN role.",
  "preconditions": "System configuration for roles open. User attempts to create a second PCC_ADMIN account.",
  "action_or_input": "User initiates process to add new PCC_ADMIN record.",
  "expected_result": "Action blocked or system logs error stating exactly one active PCC_ADMIN oversight role is maintained.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-138",
  "source_id": "BR-PMS-138",
  "purpose": "Verify PMS treats Patent Office systems as external.",
  "preconditions": "PMS receives data from Patent Office. System attempts to 'approve' or 'reject' the underlying decision internally.",
  "action_or_input": "System logic attempts to execute patent office processing logic internally.",
  "expected_result": "PMS rejects internal control attempt; system only records, tracks, notifies, logs, reports based on external data.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-139",
  "source_id": "BR-PMS-139",
  "purpose": "Verify PMS treats Financial/Payment systems as external.",
  "preconditions": "PMS attempts to execute a payment transaction directly without external system call.",
  "action_or_input": "User initiates 'Process Payment' internal function.",
  "expected_result": "Action denied; system relies on External Financial Systems for actual execution/payment.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-140",
  "source_id": "BR-PMS-140",
  "purpose": "Verify PMS limits ownership of Document systems to internal behavior.",
  "preconditions": "External DocManager System API available. PMS attempts to store full document metadata outside PMS versioning logic.",
  "action_or_input": "System logs a direct call to external DocManager without PMS wrapper/validation.",
  "expected_result": "Call rejected/Logged as external; PMS ownership limited to internal version/access audit behavior.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-141",
  "source_id": "BR-PMS-141",
  "purpose": "Verify PMS treats Prior Art DBs as external query sources.",
  "preconditions": "User searches 'Prior Art' within PMS. System attempts to store search results in local PMS DB without querying source.",
  "action_or_input": "System logic attempts to maintain local copy of prior art data.",
  "expected_result": "PMS queries external databases but treats them as query sources, not owned repositories.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-142",
  "source_id": "BR-PMS-142",
  "purpose": "Verify PMS does not control patent office filing success internally.",
  "preconditions": "External Patent Office System returns 'Success'. PMS records the ID/Date. User attempts to 'approve' the success internally.",
  "action_or_input": "System attempts to mark external filing success as an internal controlled outcome.",
  "expected_result": "PMS only records the submission details and confirmation; does not control or enforce success beyond recording.",
  "test_type": "Acceptance"
 }
]
```
