"""
Test cases for Patent Management System - Budget and Filing Operations (FR-PMS-AFR-095 to FR-PMS-AFR-102).
Generated from frozen test designs TEST-CFR-011-5 through TEST-CFR-012-3.
"""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError

from modules.patent.models import (
    PatentApplication, Budget, Filing, ApplicationHistory, OfficeAction
)
from modules.patent.services.legal import decide_budget, record_filing
from core.api.exceptions import BadRequestError as BusinessRuleViolation


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-011-5 (PMS-AFR-095) - Budget Escalation on Threshold Exceedance
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_budget_escalation_on_threshold_exceedance():
    """
    Verify escalation to higher authority on cost threshold exceedance.
    
    Source: PMS-AFR-095
    Purpose: Verify escalation to higher authority on cost threshold exceedance
    Preconditions: Total calculated budget exceeds the configured limit.
    Action: Attempt to approve the budget.
    Expected Result: The system routes/escalates the case to the higher authority instead of allowing approval.
    """
    test_id = "TEST-CFR-011-5"
    source_id = "PMS-AFR-095"
    
    # Setup: Create application and budget with total exceeding threshold
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-001",
        title="Test Application",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Test Domain",
        applicant_id=1,
        status="approved"
    )
    
    # Create budget with total exceeding threshold (threshold = 5000)
    budget = Budget.objects.create(
        application=app,
        filing_fee=3000,
        attorney_fee=2000,
        administrative_cost=1000,
        total=6000,
        status="pending",
        decided_by=None,
    )
    
    # Threshold is configured as 5000 in the service logic
    threshold = 5000
    
    # Attempt to approve budget with justification (must be >= 50 chars)
    justification = "This budget is necessary for the project."
    
    try:
        updated_budget, escalated = decide_budget(
            director_id=2,
            budget_id=budget.id,
            approve=True,
            justification=justification,
            threshold=threshold
        )
        
        # Verify escalation occurred
        assert escalated is True, "Budget should have been escalated due to exceeding threshold."
        assert updated_budget.status == "escalated", f"Budget status should be 'escalated', got '{updated_budget.status}'."
        
    except BusinessRuleViolation as e:
        pytest.fail(f"Expected escalation but received exception: {e}")


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-011-6 (PMS-AFR-096) - Budget Approval Restriction for Non-Approved Status
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_budget_approval_restriction_for_non_approved_status():
    """
    Verify restriction of budget approval for non-Approved status.
    
    Source: PMS-AFR-096
    Purpose: Verify restriction of budget approval for non-Approved status
    Preconditions: Application status is 'Submitted' (not Approved).
    Action: Director attempts to approve the associated budget.
    Expected Result: The system prevents approval with an error message.
    """
    test_id = "TEST-CFR-011-6"
    source_id = "PMS-AFR-096"
    
    # Setup: Create application in 'submitted' status (not approved)
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-002",
        title="Test Application 2",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Test Domain",
        applicant_id=1,
        status="submitted"
    )
    
    # Create budget for submitted application
    budget = Budget.objects.create(
        application=app,
        filing_fee=1000,
        attorney_fee=500,
        administrative_cost=200,
        total=1700,
        status="pending",
        decided_by=None,
    )
    
    # Attempt to approve budget (should fail due to application status)
    try:
        updated_budget, escalated = decide_budget(
            director_id=2,
            budget_id=budget.id,
            approve=True,
            justification="Budget approval needed.",
            threshold=5000
        )
        
        pytest.fail("Expected BusinessRuleViolation exception but approval succeeded.")
    except BusinessRuleViolation as e:
        # Expected - application status is not approved
        assert "Cannot propose budget" in str(e) or "Must be 'approved'" in str(e), \
            f"Expected error about application status, got: {e}"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-011-7 (PMS-AFR-097) - Budget Availability Validation Before Approval
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_budget_availability_validation_before_approval():
    """
    Verify validation of budget availability before approval.
    
    Source: PMS-AFR-097
    Purpose: Verify validation of budget availability before approval
    Preconditions: Budget data includes an 'Available' flag set to false.
    Action: Director attempts to approve the budget.
    Expected Result: The system prevents approval and indicates insufficient availability.
    """
    test_id = "TEST-CFR-011-7"
    source_id = "PMS-AFR-097"
    
    # Setup: Create application with approved status
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-003",
        title="Test Application 3",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Test Domain",
        applicant_id=1,
        status="approved"
    )
    
    # Create budget with insufficient availability (simulated by setting available=False)
    # Note: The service logic checks for 'available' flag in the data
    budget = Budget.objects.create(
        application=app,
        filing_fee=1000,
        attorney_fee=500,
        administrative_cost=200,
        total=1700,
        status="pending",
        decided_by=None,
        available=False  # Simulate insufficient availability
    )
    
    # Attempt to approve budget with justification
    try:
        updated_budget, escalated = decide_budget(
            director_id=2,
            budget_id=budget.id,
            approve=True,
            justification="Budget approval needed.",
            threshold=5000
        )
        
        pytest.fail("Expected BusinessRuleViolation exception but approval succeeded.")
    except BusinessRuleViolation as e:
        # Expected - insufficient availability
        assert "insufficient" in str(e).lower() or "available" in str(e).lower(), \
            f"Expected error about insufficient availability, got: {e}"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-011-8 (PMS-AFR-098) - Financial Transaction Logging with Authorization Info
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_financial_transaction_logging_with_authorization_info():
    """
    Verify logging of financial transactions with authorization info.
    
    Source: PMS-AFR-098
    Purpose: Verify logging of financial transactions with authorization info
    Preconditions: Budget approval is executed.
    Action: Access the Audit Logs for Financial Transactions.
    Expected Result: The log includes transaction details and the authorizing level.
    """
    test_id = "TEST-CFR-011-8"
    source_id = "PMS-AFR-098"
    
    # Setup: Create application with approved status
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-004",
        title="Test Application 4",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Test Domain",
        applicant_id=1,
        status="approved"
    )
    
    # Create budget
    budget = Budget.objects.create(
        application=app,
        filing_fee=2000,
        attorney_fee=1500,
        administrative_cost=500,
        total=4000,
        status="pending",
        decided_by=None,
    )
    
    # Execute budget approval (this should create history entry)
    updated_budget, escalated = decide_budget(
        director_id=2,
        budget_id=budget.id,
        approve=True,
        justification="Budget approved for project.",
        threshold=5000
    )
    
    # Verify history entry was created with authorization info
    history_entries = ApplicationHistory.objects.filter(
        application=app
    ).order_by('-created_at')
    
    assert history_entries.count() > 0, "Expected at least one history entry for budget approval."
    
    # Check that the last entry contains authorization info (director_id)
    latest_entry = list(history_entries)[0]
    assert latest_entry.actor_id == 2, f"Expected actor_id to be director (2), got {latest_entry.actor_id}"
    assert "Budget approved" in latest_entry.note or "justification" in str(latest_entry).lower(), \
        f"Expected authorization info in history note: {latest_entry.note}"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-012-0 (PMS-AFR-099) - Attorney Preparation of Filing Package
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_attorney_preparation_of_filing_package():
    """
    Verify Attorney preparation of filing package.
    
    Source: PMS-AFR-099
    Purpose: Verify Attorney preparation of the application package
    Preconditions: Application is ready for external filing.
    Action: Attorney navigates to 'File Application'.
    Expected Result: The system allows preparation of the application package.
    """
    test_id = "TEST-CFR-012-0"
    source_id = "PMS-AFR-099"
    
    # Setup: Create application with approved status and assigned attorney
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-005",
        title="Test Application 5",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Test Domain",
        applicant_id=1,
        status="approved"
    )
    
    # Create budget with approved status
    Budget.objects.create(
        application=app,
        filing_fee=2000,
        attorney_fee=1500,
        administrative_cost=500,
        total=4000,
        status="approved",
        decided_by=2,
    )
    
    # Create assigned attorney
    from modules.patent.models import AttorneyAssignment
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=3,
        status="accepted"
    )
    
    # Verify attorney can prepare filing package (record_filing should succeed)
    try:
        filing = record_filing(
            attorney_id=3,
            application_id=app.id,
            office="USPTO",
            filing_number="12345678",
            filing_date=date.today(),
            international=False
        )
        
        assert filing is not None, "Expected filing record to be created."
        assert filing.application == app, "Filing should be associated with the application."
        assert filing.patent_office == "USPTO", f"Expected patent office 'USPTO', got '{filing.patent_office}'."
        
    except BusinessRuleViolation as e:
        pytest.fail(f"Expected filing to succeed but received exception: {e}")


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-012-1 (PMS-AFR-100) - Filing Format Compliance Validation
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_filing_format_compliance_validation():
    """
    Verify validation of filing format compliance (if rules exist).
    
    Source: PMS-AFR-100
    Purpose: Verify validation of filing format compliance (if rules exist)
    Preconditions: Filing package includes invalid format for a specific office.
    Action: Submit the package.
    Expected Result: If valid validation rules exist, the system flags non-compliance.
    """
    test_id = "TEST-CFR-012-1"
    source_id = "PMS-AFR-100"
    
    # Setup: Create application with approved status and assigned attorney
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-006",
        title="Test Application 6",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Test Domain",
        applicant_id=1,
        status="approved"
    )
    
    # Create budget with approved status
    Budget.objects.create(
        application=app,
        filing_fee=2000,
        attorney_fee=1500,
        administrative_cost=500,
        total=4000,
        status="approved",
        decided_by=2,
    )
    
    # Create assigned attorney
    from modules.patent.models import AttorneyAssignment
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=3,
        status="accepted"
    )
    
    # Attempt to record filing with invalid format (e.g., missing required field)
    try:
        # Simulate invalid filing data (missing required fields or invalid format)
        filing = record_filing(
            attorney_id=3,
            application_id=app.id,
            office="USPTO",
            filing_number="",  # Invalid - empty filing number
            filing_date=date.today(),
            international=False
        )
        
        pytest.fail("Expected BusinessRuleViolation exception for invalid format.")
    except BusinessRuleViolation as e:
        # Expected - invalid format (empty filing number)
        assert "invalid" in str(e).lower() or "required" in str(e).lower(), \
            f"Expected error about invalid format, got: {e}"


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-012-2 (PMS-AFR-101) - Recording Indian Patent Office Submission
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_recording_indian_patent_office_submission():
    """
    Verify recording of Indian Patent Office submission.
    
    Source: PMS-AFR-101
    Purpose: Verify recording of Indian Patent Office submission
    Preconditions: Attorney prepares the package.
    Action: Record the submission to Indian Patent Office.
    Expected Result: The system logs the submission details.
    """
    test_id = "TEST-CFR-012-2"
    source_id = "PMS-AFR-101"
    
    # Setup: Create application with approved status and assigned attorney
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-007",
        title="Test Application 7",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Test Domain",
        applicant_id=1,
        status="approved"
    )
    
    # Create budget with approved status
    Budget.objects.create(
        application=app,
        filing_fee=2000,
        attorney_fee=1500,
        administrative_cost=500,
        total=4000,
        status="approved",
        decided_by=2,
    )
    
    # Create assigned attorney
    from modules.patent.models import AttorneyAssignment
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=3,
        status="accepted"
    )
    
    # Record filing to Indian Patent Office (IPO)
    try:
        filing = record_filing(
            attorney_id=3,
            application_id=app.id,
            office="IPO",  # Indian Patent Office
            filing_number="IN20241234567",
            filing_date=date.today(),
            international=False
        )
        
        assert filing is not None, "Expected filing record to be created."
        assert filing.application == app, "Filing should be associated with the application."
        assert filing.patent_office == "IPO", f"Expected patent office 'IPO', got '{filing.patent_office}'."
        assert filing.filing_number == "IN20241234567", \
            f"Expected filing number 'IN20241234567', got '{filing.filing_number}'."
        
    except BusinessRuleViolation as e:
        pytest.fail(f"Expected filing to succeed but received exception: {e}")


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-012-3 (PMS-AFR-102) - Recording International Patent Office Submission
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_recording_international_patent_office_submission():
    """
    Verify recording of International Patent Office submission.
    
    Source: PMS-AFR-102
    Purpose: Verify recording of International Patent Office submission
    Preconditions: Attorney prepares the package.
    Action: Record the submission to an international office (e.g., WIPO).
    Expected Result: The system logs the submission details.
    """
    test_id = "TEST-CFR-012-3"
    source_id = "PMS-AFR-102"
    
    # Setup: Create application with approved status and assigned attorney
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-008",
        title="Test Application 8",
        abstract="Test Abstract",
        description="Test Description",
        claims="Test Claims",
        technical_domain="Test Domain",
        applicant_id=1,
        status="approved"
    )
    
    # Create budget with approved status
    Budget.objects.create(
        application=app,
        filing_fee=2000,
        attorney_fee=1500,
        administrative_cost=500,
        total=4000,
        status="approved",
        decided_by=2,
    )
    
    # Create assigned attorney
    from modules.patent.models import AttorneyAssignment
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=3,
        status="accepted"
    )
    
    # Record filing to WIPO (World Intellectual Property Organization)
    try:
        filing = record_filing(
            attorney_id=3,
            application_id=app.id,
            office="WIPO",  # International Patent Office
            filing_number="PCT/2024/123456",
            filing_date=date.today(),
            international=True  # Mark as international filing
        )
        
        assert filing is not None, "Expected filing record to be created."
        assert filing.application == app, "Filing should be associated with the application."
        assert filing.patent_office == "WIPO", f"Expected patent office 'WIPO', got '{filing.patent_office}'."
        assert filing.filing_number == "PCT/2024/123456", \
            f"Expected filing number 'PCT/2024/123456', got '{filing.filing_number}'."
        assert filing.international is True, "Expected international flag to be True."
        
    except BusinessRuleViolation as e:
        pytest.fail(f"Expected filing to succeed but received exception: {e}")
