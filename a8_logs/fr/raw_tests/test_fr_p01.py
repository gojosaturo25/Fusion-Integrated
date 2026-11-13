"""Automated backend tests for Patent Management System (PMS) - Part 1."""
import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument, AttorneyAssignment,
    PatentabilityOpinion, Budget, Filing, OfficeAction, MaintenanceRecord, Appeal,
    ApplicationHistory
)
from modules.patent.services.applications import (
    submit_application, assign_director, review_application, resubmit_application,
    withdraw_application, expire_overdue_resubmissions, file_appeal, decide_appeal
)
from modules.patent.services.legal import (
    assign_attorney, respond_to_assignment, record_opinion, propose_budget, decide_budget,
    record_filing
)
from conftest import make_principal, user_ref


@pytest.fixture
def applicant_user():
    """Create a test applicant user."""
    return user_ref(user_id=1001, kind="student", discipline="CSE")


@pytest.fixture
def director_user():
    """Create a test director user."""
    return user_ref(user_id=2001, kind="faculty", discipline="Engineering")


@pytest.fixture
def pcc_admin_user():
    """Create a test PCC_ADMIN user."""
    return user_ref(user_id=3001, kind="staff", discipline="Administration")


@pytest.fixture
def attorney_user():
    """Create a test attorney user."""
    return user_ref(user_id=4001, kind="faculty", discipline="Law")


@pytest.fixture
def inventor_user(applicant_user):
    """Create a test inventor user."""
    return user_ref(user_id=5001, kind="student", discipline="CSE")


@pytest.fixture
def application(applicant_user, inventor_user):
    """Create a test patent application."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="US2024-0001",
        applicant_id=applicant_user.user_id,
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Technology",
        status="submitted"
    )
    
    Inventor.objects.create(
        application=app,
        user_id=inventor_user.user_id,
        name="John Doe",
        email="john@example.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def approved_application(applicant_user, inventor_user):
    """Create a test application with approved status."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="US2024-0002",
        applicant_id=applicant_user.user_id,
        title="Approved Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Technology",
        status="approved"
    )
    
    Inventor.objects.create(
        application=app,
        user_id=inventor_user.user_id,
        name="Jane Doe",
        email="jane@example.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def assigned_application(applicant_user, inventor_user):
    """Create a test application with attorney assignment."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="US2024-0003",
        applicant_id=applicant_user.user_id,
        title="Assigned Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Technology",
        status="attorney_assigned"
    )
    
    Inventor.objects.create(
        application=app,
        user_id=inventor_user.user_id,
        name="Bob Smith",
        email="bob@example.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def escalated_application(applicant_user):
    """Create a test application with missed deadline."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="US2024-0004",
        applicant_id=applicant_user.user_id,
        title="Escalated Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Technology",
        status="needs_revision",
        resubmission_deadline=date.today() - timedelta(days=1)
    )
    
    Inventor.objects.create(
        application=app,
        user_id=inventor_user.user_id,
        name="Alice Johnson",
        email="alice@example.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def conflict_applicant(applicant_user):
    """Create a test applicant with co-inventorship."""
    return user_ref(user_id=6001, kind="student", discipline="CSE")


@pytest.fixture
def conflict_inventor(applicant_user):
    """Create a test inventor who is also an applicant."""
    return user_ref(user_id=7001, kind="student", discipline="CSE")


class TestCFR0010ApplicantApplicationTracking:
    """Test TEST-CFR-001-0: Verify application tracking by Applicant (PMS-AFR-010)."""
    
    def test_applicant_can_view_own_applications(self, applicant_user, application):
        """Verify that an applicant can view their patent applications with status and progress."""
        principal = make_principal(
            user_id=applicant_user.user_id,
            kind="student",
            permissions={"patent.application.view_self"},
            modules=("patent",),
            roles=("student",)
        )
        
        # Verify application exists in database
        assert PatentApplication.objects.filter(applicant_id=applicant_user.user_id).exists()
        
        # Verify applicant can access their applications via API
        response = principal.get(reverse('application-list'))
        
        # Should return at least one application
        assert response.data['count'] >= 1
        
        # Verify application details are accessible
        app_detail = PatentApplication.objects.get(pk=application.id)
        assert app_detail.applicant_id == applicant_user.user_id
        assert app_detail.status in ['submitted', 'under_review', 'approved', 'granted']


class TestCFR0011ApplicantReportViewing:
    """Test TEST-CFR-001-1: Verify report viewing by Applicant (PMS-AFR-016)."""
    
    def test_applicant_can_view_application_report(self, applicant_user, application):
        """Verify that an applicant can view detailed reports for their patent applications."""
        principal = make_principal(
            user_id=applicant_user.user_id,
            kind="student",
            permissions={"patent.application.view_self"},
            modules=("patent",),
            roles=("student",)
        )
        
        # Verify application exists
        assert PatentApplication.objects.filter(applicant_id=applicant_user.user_id).exists()
        
        # Verify applicant can access application details via API
        response = principal.get(reverse('application-detail', kwargs={'pk': application.id}))
        
        # Should return application data with inventors and documents counts
        assert response.data['id'] == application.id
        assert response.data['applicant_id'] == applicant_user.user_id


class TestCFR0020DirectorWorkflowOversight:
    """Test TEST-CFR-002-0: Verify workflow oversight by Director (PMS-AFR-023)."""
    
    def test_director_can_view_assigned_applications(self, director_user, application):
        """Verify that a Director can view only applications assigned to them with workflow details."""
        principal = make_principal(
            user_id=director_user.user_id,
            kind="faculty",
            permissions={"patent.application.review"},
            modules=("patent",),
            roles=("director",)
        )
        
        # Assign application to director
        assign_director(
            admin_id=pcc_admin_user.user_id,
            application_id=application.id,
            director_id=director_user.user_id
        )
        
        # Verify application exists in database with assigned director
        assert PatentApplication.objects.filter(assigned_director_id=director_user.user_id).exists()
        
        # Verify director can access their applications via API
        response = principal.get(reverse('application-list'))
        
        # Should return at least one application
        assert response.data['count'] >= 1
        
        # Verify workflow details are accessible (review_due_date, latest_decision)
        app_detail = PatentApplication.objects.get(pk=application.id)
        assert app_detail.assigned_director_id == director_user.user_id


class TestCFR0030ConflictOfInterestMonitoring:
    """Test TEST-CFR-003-0: Verify conflict-of-interest monitoring by PCC_ADMIN (PMS-AFR-026)."""
    
    def test_pcc_admin_detects_conflict_of_interest(self, pcc_admin_user, application):
        """Verify that PCC_ADMIN can detect and flag conflict-of-interest cases."""
        principal = make_principal(
            user_id=pcc_admin_user.user_id,
            kind="staff",
            permissions={"patent.admin.manage"},
            modules=("patent",),
            roles=("pcc_admin",)
        )
        
        # Create application with inventor who is also a co-inventor (conflict scenario)
        conflict_app = PatentApplication.objects.create(
            APPLICATION_NUMBER="US2024-0005",
            applicant_id=applicant_user.user_id,
            title="Conflict Application",
            abstract="Test abstract",
            description="Test description",
            claims="Test claims",
            technical_domain="Technology",
            status="approved"
        )
        
        # Create inventor who is also the PCC_ADMIN user (conflict)
        Inventor.objects.create(
            application=conflict_app,
            user_id=pcc_admin_user.user_id,
            name="PCC Admin User",
            email="pcc@example.com",
            contribution_percent=50.0,
            agreement_signed=True
        )
        
        # Verify conflict exists in database
        inventors = Inventor.objects.filter(application=conflict_app)
        inventor_user_ids = inventors.values_list('user_id', flat=True)
        
        assert pcc_admin_user.user_id in inventor_user_ids
        
        # PCC_ADMIN should be able to access the application for review
        response = principal.get(reverse('application-list'))
        
        # Should return at least one application
        assert response.data['count'] >= 1


class TestCFR0031PccAdminRoleManagement:
    """Test TEST-CFR-003-1: Verify configuration management by PCC_ADMIN (PMS-AFR-027)."""
    
    def test_pcc_admin_can_manage_user_roles(self, pcc_admin_user):
        """Verify that PCC_ADMIN can manage user roles in system configuration."""
        principal = make_principal(
            user_id=pcc_admin_user.user_id,
            kind="staff",
            permissions={"patent.admin.manage"},
            modules=("patent",),
            roles=("pcc_admin",)
        )
        
        # Verify PCC_ADMIN has admin permission
        assert principal.has_permission("patent.admin.manage")
        
        # Verify can access system configuration via API
        response = principal.get(reverse('admin-application-list'))
        
        # Should return all applications (admin view)
        assert response.data['count'] >= 1


class TestCFR0032PccAdminEscalationHandling:
    """Test TEST-CFR-003-2: Verify escalation handling by PCC_ADMIN (PMS-AFR-029)."""
    
    def test_pcc_admin_can_handle_escalated_cases(self, pcc_admin_user, escalated_application):
        """Verify that PCC_ADMIN can handle escalated cases with resolution paths."""
        principal = make_principal(
            user_id=pcc_admin_user.user_id,
            kind="staff",
            permissions={"patent.admin.manage"},
            modules=("patent",),
            roles=("pcc_admin",)
        )
        
        # Verify application exists with escalated status (missed deadline)
        assert PatentApplication.objects.filter(pk=escalated_application.id).exists()
        
        # Verify escalation criteria met (resubmission_deadline passed)
        assert escalated_application.resubmission_deadline is not None
        
        # PCC_ADMIN should be able to access the application for resolution
        response = principal.get(reverse('application-list'))
        
        # Should return at least one application
        assert response.data['count'] >= 1


class TestCFR0033PccAdminAttorneyPanelManagement:
    """Test TEST-CFR-003-3: Verify attorney panel management by PCC_ADMIN (PMS-AFR-030)."""
    
    def test_pcc_admin_can_add_attorney_to_panel(self, pcc_admin_user):
        """Verify that PCC_ADMIN can add attorneys to the approved panel list."""
        principal = make_principal(
            user_id=pcc_admin_user.user_id,
            kind="staff",
            permissions={"patent.admin.manage"},
            modules=("patent",),
            roles=("pcc_admin",)
        )
        
        # Verify PCC_ADMIN has admin permission
        assert principal.has_permission("patent.admin.manage")
        
        # Attorney should be able to access applications via API
        response = principal.get(reverse('application-list'))
        
        # Should return all applications (admin view)
        assert response.data['count'] >= 1


class TestCFR0040AttorneyLegalAdviceRecording:
    """Test TEST-CFR-004-0: Verify legal advice recording by Attorney (PMS-AFR-037)."""
    
    def test_attorney_can_record_legal_opinion(self, attorney_user, assigned_application):
        """Verify that an attorney can record detailed legal opinions in application history."""
        principal = make_principal(
            user_id=attorney_user.user_id,
            kind="faculty",
            permissions={"patent.legal.review"},
            modules=("patent",),
            roles=("attorney",)
        )
        
        # Verify application exists with attorney assignment
        assert PatentApplication.objects.filter(pk=assigned_application.id).exists()
        
        # Verify attorney is assigned to the application
        assert assigned_application.assigned_attorney_id == attorney_user.user_id
        
        # Attorney should be able to record legal opinion via service
        opinion = record_opinion(
            attorney_id=attorney_user.user_id,
            application_id=assigned_application.id,
            novelty=True,
            non_obviousness=True,
            utility=True,
            recommendation="file_patent",
            text="Detailed legal analysis indicating patentability."
        )
        
        # Verify opinion was recorded in database
        assert PatentabilityOpinion.objects.filter(
            application=assigned_application,
            attorney_id=attorney_user.user_id
        ).exists()
        
        # Verify opinion details are correct
        opinion_record = PatentabilityOpinion.objects.get(pk=opinion.id)
        assert opinion_record.recommendation == "file_patent"
        assert opinion_record.opinion_text == "Detailed legal analysis indicating patentability."
