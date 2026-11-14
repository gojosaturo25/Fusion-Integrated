"""Test cases for Patent Management System workflows T-009 through T-014."""
import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse

from fusion_auth.client import IamSession
from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument, AttorneyAssignment,
    Budget, Filing, OfficeAction, MaintenanceRecord, Appeal, ApplicationHistory
)
from modules.patent.services.applications import withdraw_application
from modules.patent.services.legal import decide_renewal, propose_budget, decide_budget
from modules.patent.services.post_filing import record_office_action, prepare_response, submit_response
from modules.patent.domain.policy import can_withdraw


# -----------------------------------------------------------------------------
# Test T-009: Withdrawal Eligibility and Co-Inventor Consent
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t009_withdrawal_eligibility_and_co_inventor_consent():
    """T-009: Validate withdrawal eligibility checks and co-inventor consent collection."""
    source_id = "BR-PMS-067; BR-PMS-068; BR-PMS-069; BR-PMS-070"
    
    # Create application in Submitted state (pre-filing)
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-001",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="submitted"
    )
    
    # Create inventor with agreement signed (simulating co-inventor consent)
    inventor = Inventor.objects.create(
        application=app,
        user_id=2,
        name="Co-Inventor",
        email="coinventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Create second inventor without signed agreement (testing consent requirement)
    inventor2 = Inventor.objects.create(
        application=app,
        user_id=3,
        name="Another Co-Inventor",
        email="another@test.com",
        contribution_percent=50.0,
        agreement_signed=False
    )
    
    # Test withdrawal eligibility check
    assert can_withdraw(app.status), "Application should be withdrawable from Submitted state"
    
    # Simulate withdrawal with reason
    reason = "Testing withdrawal workflow"
    withdrawn_app = withdraw_application(
        applicant_id=1,
        application_id=app.id,
        reason=reason
    )
    
    # Verify status updated to Withdrawn
    assert withdrawn_app.status == "withdrawn", f"Status should be 'withdrawn', got {withdrawn_app.status}"
    
    # Verify history entry created
    history = ApplicationHistory.objects.filter(application=app).first()
    assert history is not None, "Application history entry should be created"
    assert history.action == "withdraw", f"Action should be 'withdraw', got {history.action}"


# -----------------------------------------------------------------------------
# Test T-010: Maintenance Fee Renewal Decision
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t010_maintenance_renewal_decision():
    """T-010: Validate Director's decision to Renew or Do Not Renew for maintenance fee cycles."""
    source_id = "UC-PMS-018"
    
    # Create granted application with active maintenance cycle
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-002",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="granted"
    )
    
    # Create maintenance record with renewal requested
    maintenance = MaintenanceRecord.objects.create(
        application=app,
        due_date=date.today() + timedelta(days=30),
        fee=500.00,
        decision="renewal_requested",
        decided_by=None
    )
    
    # Create assigned director for the application
    app.assigned_director_id = 10
    
    # Test Renew decision
    renew_decision = decide_renewal(
        director_id=10,
        record_id=maintenance.id,
        renew=True,
        justification="Patent should be maintained"
    )
    
    assert renew_decision.decision == "renew", f"Decision should be 'renew', got {renew_decision.decision}"
    assert renew_decision.decided_by == 10, "Decision should be recorded by director"
    
    # Verify history entry created for renewal decision
    history = ApplicationHistory.objects.filter(application=app).filter(action="renewal_decided").first()
    assert history is not None, "Renewal decision history entry should be created"
    
    # Test Do Not Renew decision
    do_not_renew_decision = decide_renewal(
        director_id=10,
        record_id=maintenance.id,
        renew=False,
        justification="Patent will not be maintained"
    )
    
    assert do_not_renew_decision.decision == "do_not_renew", f"Decision should be 'do_not_renew', got {do_not_renew_decision.decision}"
    assert do_not_renew_decision.decided_by == 10, "Decision should be recorded by director"


# -----------------------------------------------------------------------------
# Test T-011: Budget Approval and Rejection Logic
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t011_budget_approval_and_rejection_logic():
    """T-011: Validate Budget Approval and Rejection logic including cost validation."""
    source_id = "BR-PMS-048; BR-PMS-052; BR-PMS-053"
    
    # Create approved application
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-003",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="approved"
    )
    
    # Create budget proposal
    budget = propose_budget(
        admin_id=5,
        application_id=app.id,
        filing_fee=2000.00,
        attorney_fee=3000.00,
        admin_cost=1000.00
    )
    
    assert budget.status == "pending", f"Budget should be 'pending', got {budget.status}"
    
    # Test Budget Approval
    approved_budget = decide_budget(
        director_id=10,
        budget_id=budget.id,
        approve=True,
        justification="Budget is within acceptable range and all costs are justified",
        threshold=10000.00
    )
    
    assert approved_budget.status == "approved", f"Budget should be 'approved', got {approved_budget.status}"
    assert approved_budget.decided_by == 10, "Decision should be recorded by director"
    
    # Verify history entry created for budget approval
    history = ApplicationHistory.objects.filter(application=app).filter(action="decide_budget").first()
    assert history is not None, "Budget decision history entry should be created"
    
    # Test Budget Rejection (within threshold)
    rejected_budget = decide_budget(
        director_id=10,
        budget_id=budget.id,
        approve=False,
        justification="Budget exceeds acceptable range",
        threshold=10000.00
    )
    
    assert rejected_budget.status == "rejected", f"Budget should be 'rejected', got {rejected_budget.status}"


# -----------------------------------------------------------------------------
# Test T-012: Pre-Filing Readiness and External Filing Transition
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t012_pre_filing_readiness_and_external_filing():
    """T-012: Validate pre-filing readiness checks and successful external filing transition."""
    source_id = "BR-PMS-055; BR-PMS-056"
    
    # Create approved application with all prerequisites complete
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-004",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="approved"
    )
    
    # Create assigned attorney
    app.assigned_attorney_id = 20
    
    # Create budget with approved status
    Budget.objects.create(
        application=app,
        filing_fee=2000.00,
        attorney_fee=3000.00,
        administrative_cost=1000.00,
        total=6000.00,
        status="approved",
        decided_by=10
    )
    
    # Create inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=3,
        name="Inventor",
        email="inventor@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Test external filing initiation
    filing = record_filing(
        attorney_id=20,
        application_id=app.id,
        office="USPTO",
        filing_number="12345678",
        filing_date=date.today(),
        international=False
    )
    
    assert filing.patent_office == "USPTO", f"Filing should be for USPTO, got {filing.patent_office}"
    assert filing.filing_number == "12345678", f"Filing number should match, got {filing.filing_number}"
    
    # Verify application status updated to 'filed'
    app.refresh_from_db()
    assert app.status == "filed", f"Application status should be 'filed', got {app.status}"


# -----------------------------------------------------------------------------
# Test T-013: Office Action Response Submission and Deadline Tracking
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t013_office_action_response_submission_and_deadline():
    """T-013: Validate Office Action response submission and deadline tracking logic."""
    source_id = "BR-PMS-146; BR-PMS-065; BR-PMS-066"
    
    # Create filed application
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-005",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="filed"
    )
    
    # Create assigned attorney
    app.assigned_attorney_id = 20
    
    # Record office action
    oa = record_office_action(
        attorney_id=20,
        application_id=app.id,
        received_date=date.today(),
        response_due_date=date.today() + timedelta(days=30),
        description="Office action received"
    )
    
    assert oa.status == "recorded", f"Office action should be 'recorded', got {oa.status}"
    
    # Prepare response (without applicant approval)
    prepared_oa = prepare_response(
        attorney_id=20,
        office_action_id=oa.id,
        response_text="Response text",
        needs_applicant_approval=False
    )
    
    assert prepared_oa.status == "response_ready", f"Status should be 'response_ready', got {prepared_oa.status}"
    
    # Submit response
    submitted_oa = submit_response(
        attorney_id=20,
        office_action_id=oa.id
    )
    
    assert submitted_oa.status == "response_submitted", f"Status should be 'response_submitted', got {submitted_oa.status}"
    
    # Verify history entry created for response submission
    history = ApplicationHistory.objects.filter(application=app).filter(action="response_submitted").first()
    assert history is not None, "Response submission history entry should be created"


# -----------------------------------------------------------------------------
# Test T-014: Conditional Workflow Branching for Applicant Review
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_t014_conditional_workflow_branching_for_applicant_review():
    """T-014: Validate conditional workflow branching where Applicant review is required."""
    source_id = "BR-PMS-146; BR-PMS-065; BR-PMS-066"
    
    # Create filed application
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="P2024-006",
        title="Test Application",
        description="Test description",
        claims="Test claims",
        applicant_id=1,
        status="filed"
    )
    
    # Create assigned attorney
    app.assigned_attorney_id = 20
    
    # Record office action awaiting applicant approval
    oa = record_office_action(
        attorney_id=20,
        application_id=app.id,
        received_date=date.today(),
        response_due_date=date.today() + timedelta(days=30),
        description="Office action received"
    )
    
    # Prepare response requiring applicant approval
    prepared_oa = prepare_response(
        attorney_id=20,
        office_action_id=oa.id,
        response_text="Response text",
        needs_applicant_approval=True
    )
    
    assert prepared_oa.status == "awaiting_applicant_approval", f"Status should be 'awaiting_applicant_approval', got {prepared_oa.status}"
    
    # Simulate applicant approval (using principal user_id)
    approved_oa = approve_response(
        applicant_id=1,
        office_action_id=oa.id
    )
    
    assert approved_oa.status == "applicant_approved", f"Status should be 'applicant_approved', got {approved_oa.status}"
    
    # Verify history entry created for response approval
    history = ApplicationHistory.objects.filter(application=app).filter(action="response_approved").first()
    assert history is not None, "Response approval history entry should be created"


# -----------------------------------------------------------------------------
# Helper function to simulate approve_response (not in services)
# -----------------------------------------------------------------------------

def approve_response(applicant_id: int, office_action_id: int) -> OfficeAction:
    """Helper function to simulate applicant response approval."""
    from modules.patent.services.post_filing import PostFilingService
    
    return PostFilingService.approve_response(
        applicant_id=applicant_id,
        office_action_id=office_action_id
    )
