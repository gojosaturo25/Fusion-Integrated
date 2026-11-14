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

The frozen BR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 49 to 56 of 81; write exactly these test cases into tests/a8/br/test_br_p07.py.
```json
[
 {
  "test_id": "BR-PMS-078",
  "source_id": "BR-PMS-078",
  "purpose": "Verify PMS blocks filing if agreements are not complete.",
  "preconditions": "Inventor Agreements incomplete; Application ready for External Filing.",
  "action_or_input": "Attorney attempts to initiate 'External Filing' action.",
  "expected_result": "Action blocked; system returns error stating Inventor agreements must be complete before filing.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-082",
  "source_id": "BR-PMS-082",
  "purpose": "Verify PMS auto-numbers document versions.",
  "preconditions": "User uploads a new version of an existing document (v1) to an application with status 'Needs Revision'.",
  "action_or_input": "System processes the upload and stores the version.",
  "expected_result": "Version number automatically incremented (e.g., v2); manual numbering ignored or auto-logic enforced.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-084",
  "source_id": "BR-PMS-084",
  "purpose": "Verify PMS restricts access to previous document versions by role/status.",
  "preconditions": "Director logged in. Application status 'Under Review'. Previous version of document exists (v1).",
  "action_or_input": "Director attempts to view/download v1 via direct link or menu item not for current active doc.",
  "expected_result": "Access denied; system restricts view based on role and application status rules.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-086",
  "source_id": "BR-PMS-086",
  "purpose": "Verify PMS enforces document access control by role and status.",
  "preconditions": "PCC_ADMIN logged in. Application status 'Submitted'. Document exists.",
  "action_or_input": "PCC_ADMIN attempts to access the specific application document view.",
  "expected_result": "Access granted/controlled according to PMS rules; system ensures visibility is limited by applicable role and status rules.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-087",
  "source_id": "BR-PMS-087",
  "purpose": "Verify PMS blocks document editing outside 'Needs Revision' status.",
  "preconditions": "Application status is 'Approved'. User (Applicant) attempts to edit the main application document.",
  "action_or_input": "User clicks 'Edit Document' button.",
  "expected_result": "Action denied; system returns error stating editing permitted only when status is Needs Revision.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-088",
  "source_id": "BR-PMS-088",
  "purpose": "Verify PMS routes licensing requests to appropriate committee/Director.",
  "preconditions": "Licensing request created by Applicant. Targeting Technology Transfer Committee.",
  "action_or_input": "System processes routing logic for the request.",
  "expected_result": "Request routed to the specific Committee or Director as per institutional process configuration.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-091",
  "source_id": "BR-PMS-091",
  "purpose": "Verify PMS enforces confidentiality controls on license records.",
  "preconditions": "License agreement stored in PMS. User logged in as non-restricted role (Applicant).",
  "action_or_input": "User attempts to view sensitive clauses or export full license record.",
  "expected_result": "Access restricted; system applies confidentiality controls based on roles.",
  "test_type": "Acceptance"
 },
 {
  "test_id": "BR-PMS-092",
  "source_id": "BR-PMS-092",
  "purpose": "Verify PMS blocks appeal submission if application status is not 'Rejected'.",
  "preconditions": "Application status is 'Under Review' or 'Rejected - Final'. User attempts to file appeal.",
  "action_or_input": "User selects 'File Appeal' action.",
  "expected_result": "Action denied; system returns error stating appeals allowed only for Rejected status applications.",
  "test_type": "Acceptance"
 }
]
```
