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

The frozen FR_DESIGN.json is supplied in consecutive parts because of the model's output limit. This part contains test cases 129 to 136 of 204; write exactly these test cases into tests/a8/fr/test_fr_p17.py.
```json
[
 {
  "test_id": "TEST-CFR-019-1",
  "source_id": "PMS-AFR-159",
  "purpose": "Verify Applicant submission of technology transfer requests",
  "preconditions": "Application is in a state allowing TTR.",
  "action_or_input": "Applicant submits a Technology Transfer Request form.",
  "expected_result": "Request is recorded."
 },
 {
  "test_id": "TEST-CFR-019-2",
  "source_id": "PMS-AFR-160",
  "purpose": "Verification of routing to appropriate committee/Director",
  "preconditions": "Request is submitted.",
  "action_or_input": "Trace the workflow status.",
  "expected_result": "System routes request based on institutional process definitions."
 },
 {
  "test_id": "TEST-CFR-019-3",
  "source_id": "PMS-AFR-161",
  "purpose": "Verification of tracking negotiation process info",
  "preconditions": "Negotiation is in progress.",
  "action_or_input": "Check the case status page.",
  "expected_result": "Negotiation details (dates, parties) are tracked."
 },
 {
  "test_id": "TEST-CFR-019-4",
  "source_id": "PMS-AFR-162",
  "purpose": "Verification of recording final agreements",
  "preconditions": "Agreement is finalized.",
  "action_or_input": "View the agreement record.",
  "expected_result": "The agreement terms are stored."
 },
 {
  "test_id": "TEST-CFR-019-5",
  "source_id": "PMS-AFR-163",
  "purpose": "Verification of updating/sharing financial-system info (where integration exists)",
  "preconditions": "Integration with finance system is active.",
  "action_or_input": "Finalize the agreement with cost details.",
  "expected_result": "Financial data is exchanged or recorded in PMS/Finance."
 },
 {
  "test_id": "TEST-CFR-019-6",
  "source_id": "PMS-AFR-164",
  "purpose": "Verification of confidentiality controls for license records",
  "preconditions": "License record is created.",
  "action_or_input": "Attempt to access confidential details without clearance.",
  "expected_result": "Access is restricted."
 },
 {
  "test_id": "TEST-CFR-020-0",
  "source_id": "PMS-AFR-165",
  "purpose": "Verification of Applicant appeal filing against rejected applications",
  "preconditions": "Application status is 'Rejected'.",
  "action_or_input": "Applicant initiates an Appeal.",
  "expected_result": "Appeal case is created."
 },
 {
  "test_id": "TEST-CFR-020-1",
  "source_id": "PMS-AFR-166",
  "purpose": "Verification of appeal filing within configured time period",
  "preconditions": "Current time exceeds the allowed appeal window.",
  "action_or_input": "Applicant attempts to file an appeal.",
  "expected_result": "System blocks filing with 'Overdue' message."
 }
]
```
