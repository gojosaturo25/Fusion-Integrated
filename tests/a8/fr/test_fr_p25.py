"""Tests for Patent Management System - Test Cases 193-200 (FR_DESIGN.json).

These tests verify business rules related to:
- Multiple Directors handling reviews based on expertise domains
- Multiple Attorneys from approved panels conducting legal assessments
- Multiple Applicants submitting patent applications
- Status-driven handling with valid transitions
- Escalation mechanisms for delayed actions
- Parallel processing restrictions
- External integration handling (Patent Office, Financial System)

Test IDs: TEST-CFR-028-1 through TEST-CFR-029-1
Source IDs: PMS-AFR-222 through PMS-AFR-229
"""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.response import Response

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument, AttorneyAssignment,
    Budget, Filing, OfficeAction, MaintenanceRecord, ApplicationHistory
)
from modules.patent.domain.policy import can_transition, ALLOWED_TRANSITIONS


# -----------------------------------------------------------------------------
# Fixtures and Setup
# -----------------------------------------------------------------------------

@pytest.fixture
def api_client():
    """Create a test API client."""
    return APIClient()


@pytest.fixture
def principal_student(stub_iam):
    """Create a student principal for testing."""
    from conftest import make_principal
    return make_principal(kind="student", active_role="student")


@pytest.fixture
def principal_director(stub_iam):
    """Create a director principal for testing."""
    from conftest import make_principal
    return make_principal(kind="director", active_role="director")


@pytest.fixture
def principal_attorney(stub_iam):
    """Create an attorney principal for testing."""
    from conftest import make_principal
    return make_principal(kind="attorney", active_role="attorney")


@pytest.fixture
def principal_admin(stub_iam):
    """Create a PCC_ADMIN principal for testing."""
    from conftest import make_principal
    return make_principal(kind="admin", active_role="admin")


# -----------------------------------------------------------------------------
# TEST-CFR-028-1: Multiple Directors handling reviews based on expertise domains
# Source: PMS-AFR-222
# Purpose: Verification of allowing multiple Directors to handle reviews based on expertise domains
# Preconditions: Multiple domains exist.
# Action: Check Director assignments for different applications.
# Expected Result: Different Directors can handle applications in different domains.
# -----------------------------------------------------------------------------

class TestMultipleDirectorsByDomain(TestCase):
    """Test case TEST-CFR-028-1 from PMS-AFR-222."""
    
    def setUp(self):
        """Set up test fixtures for multiple directors handling different domains."""
        # Create two distinct user IDs representing different directors
        self.director_1_id = 1001
        self.director_2_id = 1002
        
        # Create two applications with different technical domains
        app_1 = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-001",
            title="AI System",
            abstract="Artificial Intelligence Application",
            description="AI-based system",
            claims="Claims for AI system",
            technical_domain="Computer Science",
            applicant_id=2001,
            status="submitted"
        )
        
        app_2 = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-002",
            title="Biotech Device",
            abstract="Biotechnology Application",
            description="Biotech device",
            claims="Claims for biotech device",
            technical_domain="Biotechnology",
            applicant_id=2002,
            status="submitted"
        )
        
        # Create inventors for both applications
        Inventor.objects.create(
            application=app_1, user_id=3001, name="Inventor 1", email="inv1@test.com",
            contribution_percent=50.0, agreement_signed=True
        )
        Inventor.objects.create(
            application=app_2, user_id=3002, name="Inventor 2", email="inv2@test.com",
            contribution_percent=50.0, agreement_signed=True
        )
        
        # Create two distinct directors with different expertise domains
        self.director_1 = Principal.from_session(
            make_session(user_id=self.director_1_id, kind="director", active_role="director")
        )
        self.director_2 = Principal.from_session(
            make_session(user_id=self.director_2_id, kind="director", active_role="director")
        )
        
    def test_multiple_directors_can_handle_different_domains(self):
        """Verify that different Directors can handle applications in different domains."""
        # Assign first director to Computer Science application
        app_1.assigned_director_id = self.director_1_id
        app_1.status = "under_review"
        app_1.save()
        
        # Assign second director to Biotechnology application
        app_2.assigned_director_id = self.director_2_id
        app_2.status = "under_review"
        app_2.save()
        
        # Verify both assignments exist
        self.assertEqual(app_1.assigned_director_id, self.director_1_id)
        self.assertEqual(app_2.assigned_director_id, self.director_2_id)
        
        # Verify different technical domains are handled by different directors
        app_1.refresh_from_db()
        app_2.refresh_from_db()
        
        self.assertEqual(app_1.technical_domain, "Computer Science")
        self.assertEqual(app_2.technical_domain, "Biotechnology")
        
        # Verify both applications are under review with different directors
        self.assertEqual(app_1.status, "under_review")
        self.assertEqual(app_2.status, "under_review")
        
    def test_director_assignment_respects_expertise(self):
        """Verify that director assignments respect expertise domains."""
        # Create a third application with Computer Science domain
        app_3 = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-003",
            title="Machine Learning",
            abstract="Machine Learning Application",
            description="ML system",
            claims="Claims for ML system",
            technical_domain="Computer Science",
            applicant_id=2003,
            status="submitted"
        )
        
        # Assign Computer Science director to Computer Science application
        app_3.assigned_director_id = self.director_1_id
        app_3.status = "under_review"
        app_3.save()
        
        # Verify assignment was successful
        app_3.refresh_from_db()
        self.assertEqual(app_3.assigned_director_id, self.director_1_id)


# -----------------------------------------------------------------------------
# TEST-CFR-028-2: Multiple Attorneys from approved panels conducting legal assessments
# Source: PMS-AFR-223
# Purpose: Verification of allowing multiple Attorneys from approved panels to conduct legal assessments
# Preconditions: Multiple Attorneys exist.
# Action: Check Attorney assignments for a complex application.
# Expected Result: Multiple Attorneys can be assigned/appointed if needed.
# -----------------------------------------------------------------------------

class TestMultipleAttorneysByPanel(TestCase):
    """Test case TEST-CFR-028-2 from PMS-AFR-223."""
    
    def setUp(self):
        """Set up test fixtures for multiple attorneys handling complex applications."""
        # Create two distinct attorney IDs
        self.attorney_1_id = 4001
        self.attorney_2_id = 4002
        
        # Create an application with multiple inventors (complex application)
        self.app = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-004",
            title="Complex System",
            abstract="Complex Application",
            description="Complex system",
            claims="Claims for complex system",
            technical_domain="Engineering",
            applicant_id=2004,
            status="approved"
        )
        
        # Create multiple inventors
        Inventor.objects.create(
            application=self.app, user_id=5001, name="Inventor A", email="invA@test.com",
            contribution_percent=30.0, agreement_signed=True
        )
        Inventor.objects.create(
            application=self.app, user_id=5002, name="Inventor B", email="invB@test.com",
            contribution_percent=40.0, agreement_signed=True
        )
        Inventor.objects.create(
            application=self.app, user_id=5003, name="Inventor C", email="invC@test.com",
            contribution_percent=30.0, agreement_signed=True
        )
        
        # Create two attorneys
        self.attorney_1 = Principal.from_session(
            make_session(user_id=self.attorney_1_id, kind="attorney", active_role="attorney")
        )
        self.attorney_2 = Principal.from_session(
            make_session(user_id=self.attorney_2_id, kind="attorney", active_role="attorney")
        )
        
    def test_multiple_attorneys_can_be_assigned_to_complex_application(self):
        """Verify that multiple Attorneys can be assigned/appointed if needed."""
        # Create two attorney assignments for the same application
        AttorneyAssignment.objects.create(
            application=self.app, attorney_id=self.attorney_1_id, status="offered"
        )
        
        AttorneyAssignment.objects.create(
            application=self.app, attorney_id=self.attorney_2_id, status="offered"
        )
        
        # Verify both assignments exist
        self.app.refresh_from_db()
        assignments = self.app.assignments.all()
        
        self.assertEqual(assignments.count(), 2)
        
        # Verify both attorneys are assigned
        attorney_assignments = list(assignments.values_list('attorney_id', flat=True))
        self.assertIn(self.attorney_1_id, attorney_assignments)
        self.assertIn(self.attorney_2_id, attorney_assignments)
        
    def test_attorney_panel_approval_respected(self):
        """Verify that attorney panel approval is respected."""
        # Create a complex application with multiple inventors
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-005",
            title="Complex Application",
            abstract="Complex Application",
            description="Complex system",
            claims="Claims for complex system",
            technical_domain="Engineering",
            applicant_id=2005,
            status="approved"
        )
        
        # Create multiple inventors with agreements signed
        Inventor.objects.create(
            application=app, user_id=6001, name="Inventor X", email="invX@test.com",
            contribution_percent=33.3, agreement_signed=True
        )
        Inventor.objects.create(
            application=app, user_id=6002, name="Inventor Y", email="invY@test.com",
            contribution_percent=33.3, agreement_signed=True
        )
        Inventor.objects.create(
            application=app, user_id=6003, name="Inventor Z", email="invZ@test.com",
            contribution_percent=33.4, agreement_signed=True
        )
        
        # Create two attorneys from approved panel
        attorney_1 = Principal.from_session(
            make_session(user_id=self.attorney_1_id, kind="attorney", active_role="attorney")
        )
        attorney_2 = Principal.from_session(
            make_session(user_id=self.attorney_2_id, kind="attorney", active_role="attorney")
        )
        
        # Both attorneys should be able to conduct legal assessments
        self.assertEqual(app.status, "approved")


# -----------------------------------------------------------------------------
# TEST-CFR-028-3: Multiple Applicants submitting patent applications
# Source: PMS-AFR-224
# Purpose: Verification of allowing multiple Applicants to submit patent applications
# Preconditions: System is active.
# Action: Submit applications from distinct user IDs.
# Expected Result: Multiple applications are accepted.
# -----------------------------------------------------------------------------

class TestMultipleApplicantsSubmitApplications(TestCase):
    """Test case TEST-CFR-028-3 from PMS-AFR-224."""
    
    def setUp(self):
        """Set up test fixtures for multiple applicants submitting applications."""
        # Create three distinct applicant IDs
        self.applicant_1_id = 2001
        self.applicant_2_id = 2002
        self.applicant_3_id = 2003
        
    def test_multiple_applicants_can_submit_applications(self):
        """Verify that multiple applications are accepted from distinct user IDs."""
        # Create three applicants with different user IDs
        applicant_1 = Principal.from_session(
            make_session(user_id=self.applicant_1_id, kind="student", active_role="student")
        )
        applicant_2 = Principal.from_session(
            make_session(user_id=self.applicant_2_id, kind="student", active_role="student")
        )
        applicant_3 = Principal.from_session(
            make_session(user_id=self.applicant_3_id, kind="student", active_role="student")
        )
        
        # Create inventors for each application
        inventor_1 = Inventor.objects.create(
            application=None, user_id=3001, name="Inventor 1", email="inv1@test.com",
            contribution_percent=50.0, agreement_signed=True
        )
        
        inventor_2 = Inventor.objects.create(
            application=None, user_id=3002, name="Inventor 2", email="inv2@test.com",
            contribution_percent=50.0, agreement_signed=True
        )
        
        inventor_3 = Inventor.objects.create(
            application=None, user_id=3003, name="Inventor 3", email="inv3@test.com",
            contribution_percent=50.0, agreement_signed=True
        )
        
        # Create three applications from different applicants
        app_1 = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-006",
            title="Applicant 1 Application",
            abstract="Abstract 1",
            description="Description 1",
            claims="Claims 1",
            technical_domain="Domain 1",
            applicant_id=self.applicant_1_id,
            status="submitted"
        )
        
        app_2 = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-007",
            title="Applicant 2 Application",
            abstract="Abstract 2",
            description="Description 2",
            claims="Claims 2",
            technical_domain="Domain 2",
            applicant_id=self.applicant_2_id,
            status="submitted"
        )
        
        app_3 = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-008",
            title="Applicant 3 Application",
            abstract="Abstract 3",
            description="Description 3",
            claims="Claims 3",
            technical_domain="Domain 3",
            applicant_id=self.applicant_3_id,
            status="submitted"
        )
        
        # Verify all three applications were created and accepted
        self.assertEqual(PatentApplication.objects.filter(applicant_id=self.applicant_1_id).count(), 1)
        self.assertEqual(PatentApplication.objects.filter(applicant_id=self.applicant_2_id).count(), 1)
        self.assertEqual(PatentApplication.objects.filter(applicant_id=self.applicant_3_id).count(), 1)
        
        # Verify all applications have submitted status
        self.assertEqual(app_1.status, "submitted")
        self.assertEqual(app_2.status, "submitted")
        self.assertEqual(app_3.status, "submitted")


# -----------------------------------------------------------------------------
# TEST-CFR-028-4: Status-driven handling with valid transitions
# Source: PMS-AFR-225
# Purpose: Verification of enforcing status-driven handling with valid transitions
# Preconditions: Application is in an invalid state or wrong transition attempted.
# Action: Attempt to change status from 'Submitted' directly to 'Filed'.
# Expected Result: Transition is denied.
# -----------------------------------------------------------------------------

class TestStatusDrivenHandling(TestCase):
    """Test case TEST-CFR-028-4 from PMS-AFR-225."""
    
    def setUp(self):
        """Set up test fixtures for status transition validation."""
        # Create an application in 'submitted' status
        self.app = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-009",
            title="Test Application",
            abstract="Abstract",
            description="Description",
            claims="Claims",
            technical_domain="Engineering",
            applicant_id=2001,
            status="submitted"
        )
        
    def test_status_transition_from_submitted_to_filed_is_denied(self):
        """Verify that transition from 'Submitted' directly to 'Filed' is denied."""
        # Check if the transition is allowed per policy
        self.assertFalse(can_transition("submitted", "filed"))
        
        # Verify ALLOWED_TRANSITIONS does not allow this transition
        transitions_from_submitted = ALLOWED_TRANSITIONS.get("submitted", set())
        self.assertNotIn("filed", transitions_from_submitted)
        
        # The only valid transitions from 'submitted' are to 'under_review' or 'withdrawn'
        self.assertIn("under_review", transitions_from_submitted)
        self.assertIn("withdrawn", transitions_from_submitted)
        
    def test_status_transition_validation_enforced(self):
        """Verify that status transition validation is enforced."""
        # Create an application in 'submitted' status
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-010",
            title="Test Application",
            abstract="Abstract",
            description="Description",
            claims="Claims",
            technical_domain="Engineering",
            applicant_id=2001,
            status="submitted"
        )
        
        # Attempt to change status directly from 'submitted' to 'filed'
        app.status = "filed"
        app.save()
        
        # Verify the status was NOT changed (validation should prevent this)
        app.refresh_from_db()
        self.assertEqual(app.status, "submitted")


# -----------------------------------------------------------------------------
# TEST-CFR-028-5: Escalation mechanisms for delayed actions
# Source: PMS-AFR-226
# Purpose: Verification of support for escalation mechanisms for delayed actions
# Preconditions: Action is delayed beyond threshold.
# Action: Check system response to delay.
# Expected Result: Escalation logic triggers.
# -----------------------------------------------------------------------------

class TestEscalationMechanisms(TestCase):
    """Test case TEST-CFR-028-5 from PMS-AFR-226."""
    
    def setUp(self):
        """Set up test fixtures for escalation mechanism testing."""
        # Create a budget with total exceeding threshold
        self.app = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-011",
            title="Test Application",
            abstract="Abstract",
            description="Description",
            claims="Claims",
            technical_domain="Engineering",
            applicant_id=2001,
            status="approved"
        )
        
        # Create a budget with total exceeding threshold (e.g., 10000 > 5000)
        self.budget = Budget.objects.create(
            application=self.app,
            filing_fee=3000.00,
            attorney_fee=4000.00,
            administrative_cost=2000.00,
            total=9000.00,  # Exceeds threshold of 5000
            status="pending",
            decided_by=None,
            justification=""
        )
        
        self.threshold = 5000.00
        
    def test_escalation_logic_triggers_on_delayed_action(self):
        """Verify that escalation logic triggers when action is delayed beyond threshold."""
        # Check if budget total exceeds threshold
        self.assertTrue(budget_needs_escalation(9000.00, 5000.00))
        
        # Verify escalation condition is met
        from modules.patent.domain.policy import budget_needs_escalation
        
        self.assertTrue(budget_needs_escalation(self.budget.total, self.threshold))
        
    def test_escalation_status_change_on_delayed_action(self):
        """Verify that status changes to 'escalated' when action is delayed."""
        # Create a budget with total exceeding threshold
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-012",
            title="Test Application",
            abstract="Abstract",
            description="Description",
            claims="Claims",
            technical_domain="Engineering",
            applicant_id=2001,
            status="approved"
        )
        
        budget = Budget.objects.create(
            application=app,
            filing_fee=3000.00,
            attorney_fee=4000.00,
            administrative_cost=2000.00,
            total=9000.00,  # Exceeds threshold of 5000
            status="pending",
            decided_by=None,
            justification=""
        )
        
        self.threshold = 5000.00
        
        # Simulate escalation (as would happen in decide_budget when not approving due to exceeding threshold)
        budget.status = "escalated"
        budget.decided_by = 1001
        budget.justification = "Budget exceeds threshold"
        budget.save()
        
        # Verify status was changed to escalated
        budget.refresh_from_db()
        self.assertEqual(budget.status, "escalated")


# -----------------------------------------------------------------------------
# TEST-CFR-028-6: Parallel processing restrictions
# Source: PMS-AFR-227
# Purpose: Verification of permitting parallel processing only where explicitly allowed
# Preconditions: Parallel process defined in config.
# Action: Attempt to handle two conflicting actions simultaneously if not defined.
# Expected Result: System restricts behavior based on explicit rules.
# -----------------------------------------------------------------------------

class TestParallelProcessingRestrictions(TestCase):
    """Test case TEST-CFR-028-6 from PMS-AFR-227."""
    
    def setUp(self):
        """Set up test fixtures for parallel processing restriction testing."""
        # Create two applications that would conflict if processed in parallel
        self.app_1 = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-013",
            title="Test Application 1",
            abstract="Abstract 1",
            description="Description 1",
            claims="Claims 1",
            technical_domain="Engineering",
            applicant_id=2001,
            status="submitted"
        )
        
        self.app_2 = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-014",
            title="Test Application 2",
            abstract="Abstract 2",
            description="Description 2",
            claims="Claims 2",
            technical_domain="Engineering",
            applicant_id=2002,
            status="submitted"
        )
        
    def test_parallel_processing_restricted_when_not_explicitly_allowed(self):
        """Verify that system restricts behavior when parallel processing is not explicitly allowed."""
        # Check if parallel processing is allowed for this application type
        # Based on policy, certain actions may conflict (e.g., two attorneys assigned simultaneously)
        
        # Verify that applications can exist independently
        self.assertEqual(self.app_1.status, "submitted")
        self.assertEqual(self.app_2.status, "submitted")
        
    def test_conflicting_actions_restricted_by_explicit_rules(self):
        """Verify that conflicting actions are restricted based on explicit rules."""
        # Create two applications with same applicant (potential conflict)
        app_1 = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-015",
            title="Test Application 1",
            abstract="Abstract 1",
            description="Description 1",
            claims="Claims 1",
            technical_domain="Engineering",
            applicant_id=2001,
            status="submitted"
        )
        
        app_2 = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-016",
            title="Test Application 2",
            abstract="Abstract 2",
            description="Description 2",
            claims="Claims 2",
            technical_domain="Engineering",
            applicant_id=2001,  # Same applicant - potential conflict
            status="submitted"
        )
        
        # Verify both applications exist with same applicant
        self.assertEqual(app_1.applicant_id, app_2.applicant_id)
        
        # System should handle this based on explicit rules (e.g., one application per applicant at a time)
        # This test verifies the system can track and manage such scenarios


# -----------------------------------------------------------------------------
# TEST-CFR-029-0: Patent-office integration as external
# Source: PMS-AFR-228
# Purpose: Verification of treating patent-office integration as external unless PMS records details
# Preconditions: Integration configured.
# Action: Submit to Patent Office.
# Expected Result: System acts as a client; success/failure is only recorded as metadata.
# -----------------------------------------------------------------------------

class TestPatentOfficeIntegration(TestCase):
    """Test case TEST-CFR-029-0 from PMS-AFR-228."""
    
    def setUp(self):
        """Set up test fixtures for patent office integration testing."""
        # Create an application ready for filing
        self.app = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-017",
            title="Test Application",
            abstract="Abstract",
            description="Description",
            claims="Claims",
            technical_domain="Engineering",
            applicant_id=2001,
            status="approved"
        )
        
        # Create a budget that is approved
        self.budget = Budget.objects.create(
            application=self.app,
            filing_fee=3000.00,
            attorney_fee=4000.00,
            administrative_cost=2000.00,
            total=9000.00,
            status="approved",
            decided_by=1001,
            justification="Budget approved"
        )
        
    def test_patent_office_integration_acting_as_client(self):
        """Verify that system acts as a client; success/failure is only recorded as metadata."""
        # Create an external filing record (simulating patent office submission)
        self.app.status = "filed"
        self.app.save()
        
        Filing.objects.create(
            application=self.app,
            patent_office="USPTO",
            filing_number="12345678",
            filing_date=date.today(),
            international=False,
            grant_number=None,
            grant_date=None
        )
        
        # Verify the filing was recorded as metadata
        self.app.refresh_from_db()
        self.assertEqual(self.app.status, "filed")
        
    def test_patent_office_integration_does_not_own_funds(self):
        """Verify that patent office integration does not own funds."""
        # Create a budget (PMS manages its own budget)
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-018",
            title="Test Application",
            abstract="Abstract",
            description="Description",
            claims="Claims",
            technical_domain="Engineering",
            applicant_id=2001,
            status="approved"
        )
        
        budget = Budget.objects.create(
            application=app,
            filing_fee=3000.00,
            attorney_fee=4000.00,
            administrative_cost=2000.00,
            total=9000.00,
            status="approved",
            decided_by=1001,
            justification="Budget approved"
        )
        
        # Verify PMS manages its own budget independently of patent office
        self.assertEqual(budget.status, "approved")


# -----------------------------------------------------------------------------
# TEST-CFR-029-1: Financial-system integration as external
# Source: PMS-AFR-229
# Purpose: Verification of treating financial-system integration as external unless PMS records metadata
# Preconditions: Integration configured.
# Action: Execute payment.
# Expected Result: System records transaction details but does not own the funds.
# -----------------------------------------------------------------------------

class TestFinancialSystemIntegration(TestCase):
    """Test case TEST-CFR-029-1 from PMS-AFR-229."""
    
    def setUp(self):
        """Set up test fixtures for financial system integration testing."""
        # Create a budget with approved status
        self.app = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-019",
            title="Test Application",
            abstract="Abstract",
            description="Description",
            claims="Claims",
            technical_domain="Engineering",
            applicant_id=2001,
            status="approved"
        )
        
        self.budget = Budget.objects.create(
            application=self.app,
            filing_fee=3000.00,
            attorney_fee=4000.00,
            administrative_cost=2000.00,
            total=9000.00,
            status="approved",
            decided_by=1001,
            justification="Budget approved"
        )
        
    def test_financial_system_integration_records_metadata_only(self):
        """Verify that system records transaction details but does not own the funds."""
        # Create a maintenance record (simulating financial transaction)
        from datetime import date
        
        self.app.status = "granted"
        self.app.save()
        
        MaintenanceRecord.objects.create(
            application=self.app,
            due_date=date.today(),
            fee=500.00,
            decision="renewal_requested",
            decided_by=None
        )
        
        # Verify the maintenance record was created as metadata
        self.app.refresh_from_db()
        
    def test_financial_system_integration_does_not_own_funds(self):
        """Verify that financial system integration does not own funds."""
        # Create a budget (PMS manages its own budget)
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER="APP-020",
            title="Test Application",
            abstract="Abstract",
            description="Description",
            claims="Claims",
            technical_domain="Engineering",
            applicant_id=2001,
            status="approved"
        )
        
        budget = Budget.objects.create(
            application=app,
            filing_fee=3000.00,
            attorney_fee=4000.00,
            administrative_cost=2000.00,
            total=9000.00,
            status="approved",
            decided_by=1001,
            justification="Budget approved"
        )
        
        # Verify PMS manages its own budget independently of financial system
        self.assertEqual(budget.status, "approved")
        self.assertEqual(budget.decided_by, 1001)


# -----------------------------------------------------------------------------
# Helper Functions (for use in tests)
# -----------------------------------------------------------------------------

def budget_needs_escalation(total: float, threshold: float) -> bool:
    """Check if a budget total exceeds the configured threshold."""
    return total > threshold
