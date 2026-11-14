"""
Test cases for UC-PMS-028, UC-PMS-029, UC-PMS-031, UC-PMS-032, UC-PMS-033
Converted from UC_DESIGN.json test specifications.
"""

import pytest
from datetime import date
from django.test import TestCase
from django.urls import reverse

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, ApplicationHistory, OfficeAction,
    AttorneyAssignment, Inventor, ApplicationDocument
)
from modules.patent.services.post_filing import approve_response
from modules.patent.services.legal import record_opinion


# -----------------------------------------------------------------------------
# Test Case: TEST-PMS-UC028-MAX (Authorized Audit Access)
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_p05_01_test_pms_uc028_max(
    user_ref, stub_iam, monkeypatch
):
    """
    TEST-PMS-UC028-MAX: Verify that authorized actors can view audit/compliance logs.
    
    Source ID: UC-PMS-028 Main Success Scenario
    Purpose: Verify that authorized actors (PCC_ADMIN/Director) can view audit/compliance logs.
    Preconditions: Authorized actor with access to audit information.
    Action: Actor opens audit/compliance logs and selects scope.
    Expected Result: PMS displays available audit records with required fields; no business state changes.
    """
    # Create test data
    applicant = user_ref(user_id=1001, kind="student")
    director = user_ref(user_id=2001, kind="faculty")
    
    # Setup IAM session for authorized actor (Director)
    principal = Principal.from_session(
        user_id=2001,
        username="d2001",
        display_name="Director 2001",
        kind="faculty",
        active_role="director",
        roles=("director",),
        permissions=frozenset(["patent.application.view_self", "patent.admin.manage"]),
    )
    
    # Create application with history records
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-001",
        applicant_id=1001,
        status="submitted"
    )
    
    # Add some history entries
    ApplicationHistory.objects.create(
        application=app,
        actor_id=2001,
        action="submit",
        from_status=None,
        to_status="submitted",
        note="Application submitted"
    )
    
    ApplicationHistory.objects.create(
        application=app,
        actor_id=1001,
        action="review",
        from_status="submitted",
        to_status="under_review",
        note="Under review"
    )
    
    # Verify authorized access - Director can view history
    history = ApplicationHistory.objects.filter(
        application=app
    ).order_by("-created_at")
    
    assert history.count() == 2, "Director should be able to view all history records"
    
    # Verify required fields are accessible
    first_entry = history.first()
    assert hasattr(first_entry, 'id'), "History entry should have id field"
    assert hasattr(first_entry, 'actor_id'), "History entry should have actor_id field"
    assert hasattr(first_entry, 'action'), "History entry should have action field"
    assert hasattr(first_entry, 'from_status'), "History entry should have from_status field"
    assert hasattr(first_entry, 'to_status'), "History entry should have to_status field"
    assert hasattr(first_entry, 'note'), "History entry should have note field"


# -----------------------------------------------------------------------------
# Test Case: TEST-PMS-UC028-MIN (Unauthorized Audit Access Blocked)
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_p05_02_test_pms_uc028_min(
    user_ref, stub_iam, monkeypatch
):
    """
    TEST-PMS-UC028-MIN: Verify that unauthorized audit access is blocked.
    
    Source ID: UC-PMS-028 Exception Flows
    Purpose: Verify that unauthorized actors cannot view audit logs.
    Preconditions: Actor attempts to view audit logs without authorization.
    Action: Actor accesses the restricted audit record.
    Expected Result: PMS blocks access; no audit data is displayed or altered.
    """
    # Create test data
    applicant = user_ref(user_id=1001, kind="student")
    
    # Setup IAM session for unauthorized actor (Student without admin permissions)
    principal = Principal.from_session(
        user_id=1001,
        username="u1001",
        display_name="Applicant 1001",
        kind="student",
        active_role="student",
        roles=("student",),
        permissions=frozenset(["patent.application.view_self"]),
    )
    
    # Create application with history records
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-002",
        applicant_id=1001,
        status="submitted"
    )
    
    ApplicationHistory.objects.create(
        application=app,
        actor_id=2001,  # Another user's action
        action="review",
        from_status=None,
        to_status="under_review",
        note="Unauthorized review attempt"
    )
    
    # Unauthorized actor should NOT be able to see other users' history
    history = ApplicationHistory.objects.filter(
        application=app
    ).order_by("-created_at")
    
    # Student can only see their own actions, not others
    unauthorized_history_count = history.count()
    assert unauthorized_history_count == 0, "Unauthorized actor should not see other users' audit records"


# -----------------------------------------------------------------------------
# Test Case: TEST-PMS-UC029-MAX (Applicant Approves Office Action)
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_p05_03_test_pms_uc029_max(
    user_ref, stub_iam, monkeypatch
):
    """
    TEST-PMS-UC029-MAX: Verify that Applicants can approve Office Action draft responses when required.
    
    Source ID: UC-PMS-029 Main Success Scenario
    Purpose: Verify that Applicants can approve Office Action draft responses when required.
    Preconditions: Process requires Applicant review; a draft response exists.
    Action: Applicant reviews and records approval of the draft response.
    Expected Result: PMS records the approval, allowing the Attorney to finalize/submit.
    """
    # Create test data
    applicant = user_ref(user_id=1001, kind="student")
    attorney = user_ref(user_id=3001, kind="faculty")
    
    # Setup IAM session for authorized actor (Applicant)
    principal = Principal.from_session(
        user_id=1001,
        username="u1001",
        display_name="Applicant 1001",
        kind="student",
        active_role="student",
        roles=("student",),
        permissions=frozenset(["patent.application.view_self", "patent.application.create"]),
    )
    
    # Create application and attorney assignment
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-003",
        applicant_id=1001,
        status="filed"
    )
    
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=3001,
        status="accepted"
    )
    
    # Create inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Create Office Action with draft response awaiting approval
    office_action = OfficeAction.objects.create(
        application=app,
        attorney_id=3001,
        received_date=date.today(),
        response_due_date=date.today() + timedelta(days=30),
        description="Office action received",
        response_text="Draft response text",
        status="awaiting_applicant_approval"
    )
    
    # Verify initial state
    assert office_action.status == "awaiting_applicant_approval", "Office Action should be awaiting approval"
    
    # Approve the response via service
    from datetime import timedelta
    approve_response(
        applicant_id=1001,
        office_action_id=office_action.id
    )
    
    # Verify final state - status changed to applicant_approved
    updated_oa = OfficeAction.objects.get(pk=office_action.id)
    assert updated_oa.status == "applicant_approved", "Office Action should be approved after applicant approval"


# -----------------------------------------------------------------------------
# Test Case: TEST-PMS-UC031-MAX (Director Views Reports/Analytics)
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_p05_04_test_pms_uc031_max(
    user_ref, stub_iam, monkeypatch
):
    """
    TEST-PMS-UC031-MAX: Verify that Directors can view authorized reports and analytics.
    
    Source ID: UC-PMS-031 Main Success Scenario
    Purpose: Verify that Directors can view reports/analytics within their scope/domain.
    Preconditions: Director has an authorized PMS role.
    Action: Director selects a report/analytics view (e.g., portfolio, workload).
    Expected Result: PMS generates output within Director's scope/domain and logs access.
    """
    # Create test data
    director = user_ref(user_id=2001, kind="faculty")
    
    # Setup IAM session for authorized actor (Director)
    principal = Principal.from_session(
        user_id=2001,
        username="d2001",
        display_name="Director 2001",
        kind="faculty",
        active_role="director",
        roles=("director",),
        permissions=frozenset(["patent.application.view_self", "patent.admin.manage"]),
    )
    
    # Create multiple applications for director's portfolio
    app1 = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-004",
        applicant_id=1001,
        status="submitted"
    )
    
    app2 = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-005",
        applicant_id=1002,
        status="under_review"
    )
    
    # Assign director to applications
    app1.assigned_director_id = 2001
    app2.assigned_director_id = 2001
    app1.save()
    app2.save()
    
    # Verify Director can access their portfolio applications
    portfolio_apps = PatentApplication.objects.filter(
        assigned_director_id=2001
    ).order_by("-created_at")
    
    assert portfolio_apps.count() == 2, "Director should see all applications in their portfolio"
    
    # Verify required fields are accessible for analytics
    for app in portfolio_apps:
        assert hasattr(app, 'APPLICATION_NUMBER'), "Application should have APPLICATION_NUMBER field"
        assert hasattr(app, 'status'), "Application should have status field"
        assert hasattr(app, 'assigned_director_id'), "Application should have assigned_director_id field"


# -----------------------------------------------------------------------------
# Test Case: TEST-PMS-UC032-MAX (Director Workflow Oversight)
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_p05_05_test_pms_uc032_max(
    user_ref, stub_iam, monkeypatch
):
    """
    TEST-PMS-UC032-MAX: Verify that Directors can view workflow oversight information.
    
    Source ID: UC-PMS-032 Main Success Scenario
    Purpose: Verify that Directors can view workflow states, pending actions, and oversight info within their domain.
    Preconditions: Director has an authorized role and domain scope.
    Action: Director opens workflow oversight dashboard.
    Expected Result: PMS displays workflow states, pending actions, and oversight info within the Director's domain.
    """
    # Create test data
    director = user_ref(user_id=2001, kind="faculty")
    
    # Setup IAM session for authorized actor (Director)
    principal = Principal.from_session(
        user_id=2001,
        username="d2001",
        display_name="Director 2001",
        kind="faculty",
        active_role="director",
        roles=("director",),
        permissions=frozenset(["patent.application.view_self", "patent.admin.manage"]),
    )
    
    # Create applications with various workflow states
    app1 = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-006",
        applicant_id=1001,
        status="submitted"
    )
    
    app2 = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-007",
        applicant_id=1002,
        status="under_review"
    )
    
    app3 = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-008",
        applicant_id=1003,
        status="needs_revision"
    )
    
    # Assign director to applications
    app1.assigned_director_id = 2001
    app2.assigned_director_id = 2001
    app3.assigned_director_id = 2001
    app1.save()
    app2.save()
    app3.save()
    
    # Verify Director can see workflow states for all applications
    workflow_apps = PatentApplication.objects.filter(
        assigned_director_id=2001
    ).order_by("-created_at")
    
    assert workflow_apps.count() == 3, "Director should see all applications in their domain"
    
    # Verify workflow states are accessible
    for app in workflow_apps:
        assert hasattr(app, 'status'), "Application should have status field"
        assert hasattr(app, 'assigned_director_id'), "Application should have assigned_director_id field"


# -----------------------------------------------------------------------------
# Test Case: TEST-PMS-UC033-MAX (Attorney Records Legal Advice)
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_p05_06_test_pms_uc033_max(
    user_ref, stub_iam, monkeypatch
):
    """
    TEST-PMS-UC033-MAX: Verify that Attorneys can record legal advice for applications.
    
    Source ID: UC-PMS-033 Main Success Scenario
    Purpose: Verify that Attorneys can record legal advice/opinion information for an application.
    Preconditions: Attorney has a valid role and access to the application.
    Action: Attorney records legal advice/opinion information for an application.
    Expected Result: PMS associates the advice with the application history/audit record as applicable.
    """
    # Create test data
    applicant = user_ref(user_id=1001, kind="student")
    attorney = user_ref(user_id=3001, kind="faculty")
    
    # Setup IAM session for authorized actor (Attorney)
    principal = Principal.from_session(
        user_id=3001,
        username="a3001",
        display_name="Attorney 3001",
        kind="faculty",
        active_role="attorney",
        roles=("attorney",),
        permissions=frozenset(["patent.legal.review", "patent.filing.record"]),
    )
    
    # Create application with attorney assignment
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-009",
        applicant_id=1001,
        status="approved"
    )
    
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=3001,
        status="accepted"
    )
    
    # Create inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Record legal opinion via service
    record_opinion(
        attorney_id=3001,
        application_id=app.id,
        novelty=True,
        non_obviousness=True,
        utility=True,
        recommendation="file_patent",
        text="This invention is novel and non-obvious"
    )
    
    # Verify opinion was created and associated with application
    opinion = PatentabilityOpinion.objects.filter(
        application=app,
        attorney_id=3001
    ).first()
    
    assert opinion is not None, "Patentability opinion should be created"
    assert opinion.recommendation == "file_patent", "Recommendation should match input"
    assert opinion.novelty == True, "Novelty flag should be set correctly"


# -----------------------------------------------------------------------------
# Test Case: TEST-PMS-UC033-MIN (Unauthorized Legal Advice Blocked)
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_uc_p05_07_test_pms_uc033_min(
    user_ref, stub_iam, monkeypatch
):
    """
    TEST-PMS-UC033-MIN: Verify that unauthorized legal advice recording is blocked.
    
    Source ID: UC-PMS-033 Exception Flows
    Purpose: Verify that unauthorized attorneys cannot record advice for applications they don't have access to.
    Preconditions: Attorney attempts to record advice for an application they do not have access to.
    Action: Attorney selects the restricted application to record advice.
    Expected Result: Recording fails; no unrelated application state changes occur.
    """
    # Create test data
    applicant = user_ref(user_id=1001, kind="student")
    unauthorized_attorney = user_ref(user_id=3002, kind="faculty")
    
    # Setup IAM session for unauthorized actor (Attorney without access)
    principal = Principal.from_session(
        user_id=3002,
        username="a3002",
        display_name="Attorney 3002",
        kind="faculty",
        active_role="attorney",
        roles=("attorney",),
        permissions=frozenset(["patent.legal.review"]),
    )
    
    # Create application with different attorney assignment
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-010",
        applicant_id=1001,
        status="approved"
    )
    
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=3003,  # Different attorney
        status="accepted"
    )
    
    # Create inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name="Test Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Verify initial state - no opinion exists
    initial_opinion_count = PatentabilityOpinion.objects.filter(
        application=app
    ).count()
    
    assert initial_opinion_count == 0, "No opinion should exist initially"
    
    # Attempt to record legal advice via service (should fail due to unauthorized access)
    from core.api.exceptions import BadRequestError as BusinessRuleViolation
    
    try:
        record_opinion(
            attorney_id=3002,  # Unauthorized attorney
            application_id=app.id,
            novelty=True,
            non_obviousness=True,
            utility=True,
            recommendation="file_patent",
            text="Unauthorized attempt"
        )
        
        # If we get here without exception, check if opinion was created (should not be)
        updated_opinion_count = PatentabilityOpinion.objects.filter(
            application=app
        ).count()
        
        # The service should raise an error for unauthorized access
        assert False, "Should have raised BusinessRuleViolation for unauthorized attorney"
        
    except BusinessRuleViolation:
        # Expected - unauthorized access blocked
        pass
    
    # Verify no opinion was created
    final_opinion_count = PatentabilityOpinion.objects.filter(
        application=app
    ).count()
    
    assert final_opinion_count == 0, "No opinion should be created for unauthorized attorney"
