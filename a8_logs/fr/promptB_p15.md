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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 113 to 120 of 204; write exactly these test cases into tests/a8/fr/test_fr_p15.py.
```json
[
 {
  "test_id": "TEST-CFR-017-2",
  "source_id": "PMS-AFR-143",
  "purpose": "Verify querying of relevant patent databases (where integration exists)",
  "preconditions": "Search query is entered.",
  "action_or_input": "Execute search.",
  "expected_result": "System queries integrated patent database if available."
 },
 {
  "test_id": "TEST-CFR-017-3",
  "source_id": "PMS-AFR-144",
  "purpose": "Verify querying of relevant publication databases (where integration exists)",
  "preconditions": "Search query includes publication filter.",
  "action_or_input": "Execute search.",
  "expected_result": "System queries integrated publication database if available."
 },
 {
  "test_id": "TEST-CFR-017-4",
  "source_id": "PMS-AFR-145",
  "purpose": "Verify display of search results with relevance ranking",
  "preconditions": "Search returns results.",
  "action_or_input": "View the search result list.",
  "expected_result": "Results are displayed in order of relevance."
 },
 {
  "test_id": "TEST-CFR-017-5",
  "source_id": "PMS-AFR-146",
  "purpose": "Verify attachment of selected prior-art references to application",
  "preconditions": "Reference is available in search results.",
  "action_or_input": "Attach the reference to an active application.",
  "expected_result": "The reference is linked to the application document."
 },
 {
  "test_id": "TEST-CFR-017-6",
  "source_id": "PMS-AFR-147",
  "purpose": "Verify logging of prior-art search sessions for audit trail",
  "preconditions": "Search is performed.",
  "action_or_input": "Access Audit Logs for 'Search' events.",
  "expected_result": "Search session details are logged."
 },
 {
  "test_id": "TEST-CFR-017-7",
  "source_id": "PMS-AFR-148",
  "purpose": "Verify keyword optimization support for search",
  "preconditions": "Search is being executed.",
  "action_or_input": "Use suggested terms or synonym features.",
  "expected_result": "System utilizes the optimization to improve results."
 },
 {
  "test_id": "TEST-CFR-017-8",
  "source_id": "PMS-AFR-149",
  "purpose": "Verify classification mapping support for search",
  "preconditions": "Search is being executed.",
  "action_or_input": "Select a specific IPC/CPC classification.",
  "expected_result": "System uses the mapping to filter or guide results."
 },
 {
  "test_id": "TEST-CFR-018-0",
  "source_id": "PMS-AFR-150",
  "purpose": "Verify maintenance of version history for application documents",
  "preconditions": "Documents are uploaded.",
  "action_or_input": "Navigate to document repository.",
  "expected_result": "Version history is displayed."
 }
]
```
