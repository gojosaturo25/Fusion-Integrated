"""Test cases for Patent Management System UC scenarios (UC-PMS-008 to UC-PMS-015).

These tests verify business rules and exception flows for:
- Director review decisions with justification validation
- Attorney assignment from approved panel
- Non-panel attorney assignment restrictions
- Attorney acceptance/decline of assignments
- Patentability opinion recording
- External patent filing submission
- Office action response submission
"""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.response import Response

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument, AttorneyAssignment,
    PatentabilityOpinion, Budget, Filing, OfficeAction, ApplicationHistory
)
from modules.patent.services.applications import (
    review_application, resubmit_application, withdraw_application
)
from modules.patent.services.legal import (
    assign_attorney, respond_to_assignment, record_opinion, record_filing,
    prepare_response, submit_response
)
from modules.patent.domain.policy import validate_justification


# -----------------------------------------------------------------------------
# Fixtures and Test Setup
# -----------------------------------------------------------------------------

@pytest.fixture
def stub_iam(monkeypatch):
    """Use the existing stub_iam fixture from conftest.py"""
    from conftest import stub_iam
    return stub_iam(monkeypatch)


@pytest.fixture
def principal_applicant(stub_iam):
    """Create a Principal with applicant role and permissions."""
    user = stub_iam.users.get(1001, {})
    if not user:
        stub_iam.users[1001] = {
            'id': 1001,
            'username': 'u1001',
            'display_name': 'Applicant User',
            'kind': 'student',
            'discipline': 'CSE'
        }
    return Principal.from_session(
        user_id=1001,
        username='u1001',
        display_name='Applicant User',
        kind='student',
        active_role='student',
        permissions=frozenset([
            'patent.application.view_self',
            'patent.application.create',
            'patent.application.withdraw'
        ]),
        modules=('patent',)
    )


@pytest.fixture
def principal_director(stub_iam):
    """Create a Principal with director role and permissions."""
    user = stub_iam.users.get(2001, {})
    if not user:
        stub_iam.users[2001] = {
            'id': 2001,
            'username': 'u2001',
            'display_name': 'Director User',
            'kind': 'faculty',
            'discipline': 'CSE'
        }
    return Principal.from_session(
        user_id=2001,
        username='u2001',
        display_name='Director User',
        kind='faculty',
        active_role='director',
        permissions=frozenset([
            'patent.application.review',
            'patent.budget.approve',
            'patent.maintenance.manage',
            'patent.appeal.review'
        ]),
        modules=('patent',)
    )


@pytest.fixture
def principal_admin(stub_iam):
    """Create a Principal with PCC_ADMIN role and permissions."""
    user = stub_iam.users.get(3001, {})
    if not user:
        stub_iam.users[3001] = {
            'id': 3001,
            'username': 'u3001',
            'display_name': 'Admin User',
            'kind': 'staff',
            'discipline': 'IT'
        }
    return Principal.from_session(
        user_id=3001,
        username='u3001',
        display_name='Admin User',
        kind='staff',
        active_role='admin',
        permissions=frozenset([
            'patent.admin.manage',
            'patent.application.manage',
            'patent.legal.review',
            'patent.budget.approve',
            'patent.filing.record'
        ]),
        modules=('patent',)
    )


@pytest.fixture
def principal_attorney(stub_iam):
    """Create a Principal with attorney role and permissions."""
    user = stub_iam.users.get(4001, {})
    if not user:
        stub_iam.users[4001] = {
            'id': 4001,
            'username': 'u4001',
            'display_name': 'Attorney User',
            'kind': 'staff',
            'discipline': 'IT'
        }
    return Principal.from_session(
        user_id=4001,
        username='u4001',
        display_name='Attorney User',
        kind='staff',
        active_role='attorney',
        permissions=frozenset([
            'patent.legal.review',
            'patent.filing.record',
            'patent.maintenance.manage'
        ]),
        modules=('patent',)
    )


@pytest.fixture
def application(applicant, stub_iam):
    """Create a test patent application with required fields."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-001',
        applicant_id=1001,
        title='Test Patent Application',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor',
        email='inventor@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def application_with_budget(applicant, stub_iam):
    """Create a test patent application with approved budget."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-002',
        applicant_id=1001,
        title='Test Patent Application 2',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 2',
        email='inventor2@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add approved budget
    Budget.objects.create(
        application=app,
        filing_fee=1000.00,
        attorney_fee=500.00,
        administrative_cost=200.00,
        total=1700.00,
        status='approved',
        decided_by=3001,
        justification='Budget approved for filing.'
    )
    
    return app


@pytest.fixture
def application_with_office_action(applicant, stub_iam):
    """Create a test patent application with office action."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-003',
        applicant_id=1001,
        title='Test Patent Application 3',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='filed'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 3',
        email='inventor3@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add office action
    OfficeAction.objects.create(
        application=app,
        received_date=date.today() - timedelta(days=10),
        response_due_date=date.today() + timedelta(days=30),
        description='Office action received from patent office.',
        status='recorded'
    )
    
    return app


@pytest.fixture
def application_with_attorney(applicant, stub_iam):
    """Create a test patent application with assigned attorney."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-004',
        applicant_id=1001,
        title='Test Patent Application 4',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 4',
        email='inventor4@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add attorney assignment (offered status)
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=4001,
        status='offered'
    )
    
    return app


@pytest.fixture
def application_with_pending_assignment(applicant, stub_iam):
    """Create a test patent application with pending attorney assignment."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-005',
        applicant_id=1001,
        title='Test Patent Application 5',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 5',
        email='inventor5@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add attorney assignment (accepted status)
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=4001,
        status='accepted'
    )
    
    return app


@pytest.fixture
def application_with_opinion(applicant, stub_iam):
    """Create a test patent application with patentability opinion."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-006',
        applicant_id=1001,
        title='Test Patent Application 6',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 6',
        email='inventor6@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add attorney assignment (accepted status)
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=4001,
        status='accepted'
    )
    
    return app


@pytest.fixture
def application_with_filing(applicant, stub_iam):
    """Create a test patent application with filed record."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-007',
        applicant_id=1001,
        title='Test Patent Application 7',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='filed'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 7',
        email='inventor7@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add filing record
    Filing.objects.create(
        application=app,
        patent_office='USPTO',
        filing_number='12345678',
        filing_date=date.today(),
        international=False
    )
    
    return app


@pytest.fixture
def application_with_unsigned_agreement(applicant, stub_iam):
    """Create a test patent application with inventor who hasn't signed agreement."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-008',
        applicant_id=1001,
        title='Test Patent Application 8',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor WITHOUT signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 8',
        email='inventor8@test.com',
        contribution_percent=50.0,
        agreement_signed=False
    )
    
    return app


@pytest.fixture
def application_with_unapproved_budget(applicant, stub_iam):
    """Create a test patent application with unapproved budget."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER='APP-2024-009',
        applicant_id=1001,
        title='Test Patent Application 9',
        abstract='A test patent for automation.',
        description='Detailed description of the invention.',
        claims='Claims text here.',
        technical_domain='Software Engineering',
        status='approved'
    )
    
    # Add inventor with signed agreement
    Inventor.objects.create(
        application=app,
        user_id=1001,
        name='Test Inventor 9',
        email='inventor9@test.com',
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    # Add unapproved budget (pending status)
    Budget.objects.create(
        application=app,
        filing_fee=1000.00,
        attorney_fee=500.00,
        administrative_cost=200.00,
        total=1700.00,
        status='pending',
        decided_by=None,
        justification='Budget pending approval.'
    )
    
    return app


# -----------------------------------------------------------------------------
# Test Cases
# -----------------------------------------------------------------------------

class TestPMSUC008MIN:
    """Test UC-PMS-008 Exception Flows (No Justification)."""
    
    def test_director_review_decision_without_sufficient_justification(self, principal_director, application):
        """
        TEST-PMS-UC008-MIN - Verify that review decisions without sufficient justification are rejected.
        
        Purpose: Verify that review decisions without 50+ character justification fail validation.
        Preconditions: Director attempts to submit a decision with fewer than 50 characters of justification.
        Expected Result: PMS rejects the decision; no business state changes occur.
        """
        # Arrange
        short_justification = "This is too short"  # Less than 50 characters
        
        # Act - Attempt to submit review with insufficient justification
        try:
            result = review_application(
                director_id=2001,
                application_id=application.id,
                decision='reject',
                justification=short_justification
            )
            # Assert - Should raise ValueError due to validation failure
            assert False, "Expected ValueError to be raised for insufficient justification"
        except ValueError as e:
            # Assert - Verify the error message indicates justification requirement
            assert '50' in str(e) or 'justification' in str(e).lower()
        
        # Assert - Application status should not change
        application.refresh_from_db()
        assert application.status == 'approved', "Application status should remain unchanged"


class TestPMSUC010MAX:
    """Test UC-PMS-010 Main Success Scenario."""
    
    def test_pcc_admin_assign_attorney_to_approved_application(self, principal_admin, application_with_budget):
        """
        TEST-PMS-UC010-MAX - Verify that approved applications can be assigned attorneys from the approved panel.
        
        Purpose: Verify that PCC_ADMIN can assign an attorney to an approved application.
        Preconditions: Application status is Approved; PCC_ADMIN is authorized.
        Expected Result: PMS records the assignment, notifies the Attorney for acceptance/decline, and updates status to Attorney Assigned/Pending Review.
        """
        # Arrange
        admin_principal = principal_admin
        
        # Act - Assign attorney to approved application
        assignment = assign_attorney(
            admin_id=3001,
            application_id=application_with_budget.id,
            attorney_id=4001
        )
        
        # Assert - Assignment should be created with 'offered' status
        assert assignment.status == 'offered', "Assignment should be created with offered status"
        
        # Assert - Application status should update to 'attorney_assigned'
        application_with_budget.refresh_from_db()
        assert application_with_budget.status == 'attorney_assigned', "Application status should update to attorney_assigned"
        
        # Assert - History entry should be created
        history = ApplicationHistory.objects.filter(
            application=application_with_budget,
            action='assign_attorney'
        ).first()
        assert history is not None, "History entry should be created for assignment"


class TestPMS010MIN:
    """Test UC-PMS-010 Exception Flows (Non-Panel)."""
    
    def test_non_panel_attorney_assignment_blocked_without_exception(self, principal_admin, application_with_budget):
        """
        TEST-PMS-010-MIN - Verify that non-panel attorneys are only assigned if an institutional exception exists.
        
        Purpose: Verify that PMS blocks assignment of non-panel attorneys without institutional exception.
        Preconditions: PCC_ADMIN attempts to assign an attorney not in the approved panel without a recorded exception.
        Expected Result: PMS blocks assignment unless a valid institutional exception is recorded/allowed.
        """
        # Arrange - Use a different attorney ID (simulating non-panel attorney)
        non_panel_attorney_id = 5001
        
        # Act - Attempt to assign non-panel attorney
        try:
            assignment = assign_attorney(
                admin_id=3001,
                application_id=application_with_budget.id,
                attorney_id=non_panel_attorney_id
            )
            # Assert - Should raise BusinessRuleViolation due to conflict/exception check
            assert False, "Expected BusinessRuleViolation to be raised for non-panel attorney"
        except Exception as e:
            # Assert - Verify the error indicates assignment was blocked
            assert 'conflict' in str(e).lower() or 'exception' in str(e).lower(), \
                f"Expected conflict/exception error, got: {e}"
        
        # Assert - Application status should not change
        application_with_budget.refresh_from_db()
        assert application_with_budget.status == 'attorney_assigned', "Application status should remain unchanged"


class TestPMSUC011MAX:
    """Test UC-PMS-011 Main Success Scenario."""
    
    def test_attorney_accepts_or_declines_assignment(self, principal_attorney, application_with_pending_assignment):
        """
        TEST-PMS-UC011-MAX - Verify that Attorneys can accept or decline assignments.
        
        Purpose: Verify that attorney acceptance/decline updates application status appropriately.
        Preconditions: An assignment to the Attorney exists and is active.
        Expected Result: PMS records response. Acceptance updates status to Attorney Assigned; Decline updates to Pending Review and notifies PCC_ADMIN.
        """
        # Arrange - Application already has accepted attorney assignment
        
        # Act - Test acceptance
        application_with_pending_assignment.refresh_from_db()
        
        # Accept the assignment (should be already accepted, but test the logic)
        result = respond_to_assignment(
            attorney_id=4001,
            assignment_id=application_with_pending_assignment.assignments.first().id,
            accept=True,
            reason=''
        )
        
        # Assert - Application status should remain 'attorney_assigned' after acceptance
        application_with_pending_assignment.refresh_from_db()
        assert application_with_pending_assignment.status == 'attorney_assigned', \
            "Application status should remain attorney_assigned after acceptance"
        
        # Act - Test decline (simulate by creating new assignment with declined status)
        application_decline = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-2024-010',
            applicant_id=1001,
            title='Test Patent Application 10',
            abstract='A test patent for automation.',
            description='Detailed description of the invention.',
            claims='Claims text here.',
            technical_domain='Software Engineering',
            status='approved'
        )
        
        Inventor.objects.create(
            application=application_decline,
            user_id=1001,
            name='Test Inventor 10',
            email='inventor10@test.com',
            contribution_percent=50.0,
            agreement_signed=True
        )
        
        AttorneyAssignment.objects.create(
            application=application_decline,
            attorney_id=4001,
            status='offered'
        )
        
        # Act - Decline the assignment
        result = respond_to_assignment(
            attorney_id=4001,
            assignment_id=application_decline.assignments.first().id,
            accept=False,
            reason='This is a test decline reason that is too short'  # Less than 50 chars
        )
        
        # Assert - Should raise due to insufficient justification for decline
        assert False, "Expected BusinessRuleViolation for insufficient decline reason"
        
        # Act - Test with sufficient justification
        application_decline2 = PatentApplication.objects.create(
            APPLICATION_NUMBER='APP-2024-011',
            applicant_id=1001,
            title='Test Patent Application 11',
            abstract='A test patent for automation.',
            description='Detailed description of the invention.',
            claims='Claims text here.',
            technical_domain='Software Engineering',
            status='approved'
        )
        
        Inventor.objects.create(
            application=application_decline2,
            user_id=1001,
            name='Test Inventor 11',
            email='inventor11@test.com',
            contribution_percent=50.0,
            agreement_signed=True
        )
        
        AttorneyAssignment.objects.create(
            application=application_decline2,
            attorney_id=4001,
            status='offered'
        )
        
        # Act - Decline with sufficient justification
        result = respond_to_assignment(
            attorney_id=4001,
            assignment_id=application_decline2.assignments.first().id,
            accept=False,
            reason='This is a test decline reason that meets the minimum length requirement of fifty characters or more for proper documentation purposes.'
        )
        
        # Assert - Application status should update to 'approved' after decline
        application_decline2.refresh_from_db()
        assert application_decline2.status == 'approved', "Application status should update to approved after attorney decline"


class TestPMSUC012MAX:
    """Test UC-PMS-012 Main Success Scenario."""
    
    def test_attorney_records_patentability_opinion(self, principal_attorney, application_with_opinion):
        """
        TEST-PMS-UC012-MAX - Verify that Attorneys record patentability opinions with valid recommendations.
        
        Purpose: Verify that attorney can record opinion with File Patent, Do Not File, or Needs Amendment recommendation.
        Preconditions: Attorney has an assigned application and access to review details.
        Expected Result: PMS records the opinion/recommendation and notifies stakeholders.
        """
        # Arrange - Application already has accepted attorney assignment
        
        # Act - Record patentability opinion with 'file_patent' recommendation
        opinion = record_opinion(
            attorney_id=4001,
            application_id=application_with_opinion.id,
            novelty=True,
            non_obviousness=True,
            utility=True,
            recommendation='file_patent',
            text='This invention is novel, non-obvious, and useful.'
        )
        
        # Assert - Opinion should be created with correct values
        assert opinion.recommendation == 'file_patent', "Recommendation should be file_patent"
        assert opinion.novelty == True, "Novelty should be True"
        assert opinion.non_obviousness == True, "Non-obviousness should be True"
        assert opinion.utility == True, "Utility should be True"
        
        # Assert - History entry should be created
        history = ApplicationHistory.objects.filter(
            application=application_with_opinion,
            action='record_opinion'
        ).first()
        assert history is not None, "History entry should be created for opinion recording"


class TestPMSUC013MAX:
    """Test UC-PMS-013 Main Success Scenario."""
    
    def test_attorney_submits_external_filing(self, principal_attorney, application_with_filing):
        """
        TEST-PMS-UC013-MAX - Verify that Attorneys can prepare, validate, and record external patent filings.
        
        Purpose: Verify that attorney can submit external filing when prerequisites are met.
        Preconditions: Required approvals, budget allocation, and inventor agreements are complete; Attorney has filing authority.
        Expected Result: PMS sets application status to Filed, records audit/history, and triggers confirmation notification.
        """
        # Arrange - Application already has filing record
        
        # Act - Record new external filing
        filing = record_filing(
            attorney_id=4001,
            application_id=application_with_filing.id,
            office='USPTO',
            filing_number='87654321',
            filing_date=date.today(),
            international=True
        )
        
        # Assert - Filing should be created with correct values
        assert filing.patent_office == 'USPTO', "Patent office should be USPTO"
        assert filing.filing_number == '87654321', "Filing number should match"
        assert filing.international == True, "International flag should be True"
        
        # Assert - Application status should update to 'filed'
        application_with_filing.refresh_from_db()
        assert application_with_filing.status == 'filed', "Application status should be filed"
        
        # Assert - History entry should be created
        history = ApplicationHistory.objects.filter(
            application=application_with_filing,
            action='record_filing'
        ).first()
        assert history is not None, "History entry should be created for filing recording"


class TestPMSUC013MIN:
    """Test UC-PMS-013 Exception Flows (Prerequisites)."""
    
    def test_external_filing_blocked_if_prerequisites_missing(self, principal_attorney, application_with_unapproved_budget):
        """
        TEST-PMS-UC013-MIN - Verify that external filing is blocked if prerequisite approvals or agreements are missing.
        
        Purpose: Verify that PMS blocks filing when budget approval or inventor agreement is missing.
        Preconditions: Required budget approval or inventor agreement is missing for the application.
        Expected Result: PMS blocks the filing action.
        """
        # Arrange - Application has unapproved budget (pending status)
        
        # Act - Attempt to record filing with unapproved budget
        try:
            filing = record_filing(
                attorney_id=4001,
                application_id=application_with_unapproved_budget.id,
                office='USPTO',
                filing_number='11111111',
                filing_date=date.today(),
                international=False
            )
            # Assert - Should raise BusinessRuleViolation due to unapproved budget
            assert False, "Expected BusinessRuleViolation to be raised for unapproved budget"
        except Exception as e:
            # Assert - Verify the error indicates prerequisite issue
            assert 'budget' in str(e).lower() or 'approval' in str(e).lower(), \
                f"Expected budget/approval error, got: {e}"
        
        # Assert - Application status should not change
        application_with_unapproved_budget.refresh_from_db()
        assert application_with_unapproved_budget.status == 'approved', "Application status should remain unchanged"


class TestPMSUC015MAX:
    """Test UC-PMS-015 Main Success Scenario."""
    
    def test_attorney_submits_office_action_response(self, principal_attorney, application_with_office_action):
        """
        TEST-PMS-UC015-MAX - Verify that Attorneys can submit office-action responses, handling optional Applicant review.
        
        Purpose: Verify that attorney can prepare and submit office action response.
        Preconditions: Office action exists; Attorney has access; applicable deadline/extension data is available.
        Expected Result: PMS updates response tracking, audit/history, and maintains status. Extension requests are recorded if allowed.
        """
        # Arrange - Application already has office action with 'recorded' status
        
        # Act - Prepare response without applicant approval needed
        updated_oa = prepare_response(
            attorney_id=4001,
            office_action_id=application_with_office_action.office_actions.first().id,
            response_text='This is a prepared response to the office action.',
            needs_applicant_approval=False
        )
        
        # Assert - Office action status should update to 'response_ready'
        updated_oa.refresh_from_db()
        assert updated_oa.status == 'response_ready', "Office action status should be response_ready"
        
        # Act - Submit the response
        submitted_oa = submit_response(
            attorney_id=4001,
            office_action_id=updated_oa.id
        )
        
        # Assert - Office action status should update to 'response_submitted'
        submitted_oa.refresh_from_db()
        assert submitted_oa.status == 'response_submitted', "Office action status should be response_submitted"
        
        # Assert - History entry should be created for both prepare and submit actions
        history_prepare = ApplicationHistory.objects.filter(
            application=application_with_office_action,
            action='response_prepared'
        ).first()
        assert history_prepare is not None, "History entry should be created for response preparation"
        
        history_submit = ApplicationHistory.objects.filter(
            application=application_with_office_action,
            action='response_submitted'
        ).first()
        assert history_submit is not None, "History entry should be created for response submission"
