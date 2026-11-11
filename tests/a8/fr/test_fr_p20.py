"""Test cases for report generation functionality (TEST-CFR-022-1 to TEST-CFR-022-8).

Source: PMS-AFR-183 through PMS-AFR-190
Role: PCC_ADMIN/Director
"""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.response import Response

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Budget, ApplicationDocument, Inventor,
    AttorneyAssignment, PatentabilityOpinion, Filing, OfficeAction,
    MaintenanceRecord, Appeal, ApplicationHistory
)


@pytest.fixture
def api_client():
    """Create a test API client."""
    return APIClient()


@pytest.fixture
def principal():
    """Create a Principal with PCC_ADMIN role for report generation tests."""
    from conftest import make_principal
    return make_principal(kind="admin", roles=("PCC_ADMIN",))


@pytest.fixture
def director_principal():
    """Create a Principal with Director role for report generation tests."""
    from conftest import make_principal
    return make_principal(kind="director", roles=("Director",))


@pytest.fixture
def sample_application(principal):
    """Create a sample patent application for testing."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="US2024-001",
        title="Test Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Technology",
        applicant_id=principal.user_id,
        status="approved",
    )
    return app


@pytest.fixture
def sample_budget(sample_application):
    """Create a sample budget for testing."""
    budget = Budget.objects.create(
        application=sample_application,
        filing_fee=1000.00,
        attorney_fee=500.00,
        administrative_cost=200.00,
        total=1700.00,
        status="approved",
    )
    return budget


@pytest.fixture
def sample_inventor(sample_application):
    """Create a sample inventor for testing."""
    inventor = Inventor.objects.create(
        application=sample_application,
        user_id=principal.user_id,
        name="Test Inventor",
        email="test@example.com",
        contribution_percent=50.0,
        agreement_signed=True,
    )
    return inventor


@pytest.fixture
def sample_filing(sample_application):
    """Create a sample filing for testing."""
    filing = Filing.objects.create(
        application=sample_application,
        patent_office="USPTO",
        filing_number="12345678",
        filing_date=date(2024, 1, 1),
        international=False,
    )
    return filing


@pytest.fixture
def sample_maintenance(sample_application):
    """Create a sample maintenance record for testing."""
    maintenance = MaintenanceRecord.objects.create(
        application=sample_application,
        due_date=date(2024, 6, 1),
        fee=500.00,
        decision="renew",
        decided_by=principal.user_id,
    )
    return maintenance


@pytest.fixture
def sample_office_action(sample_application):
    """Create a sample office action for testing."""
    oa = OfficeAction.objects.create(
        application=sample_application,
        received_date=date(2024, 2, 1),
        response_due_date=date(2024, 3, 1),
        description="Office action description",
        status="recorded",
    )
    return oa


@pytest.fixture
def sample_appeal(sample_application):
    """Create a sample appeal for testing."""
    appeal = Appeal.objects.create(
        application=sample_application,
        grounds="Appeal grounds",
        status="submitted",
        decided_by=None,
        justification="",
    )
    return appeal


@pytest.fixture
def report_scheduled(principal):
    """Create a scheduled report for testing."""
    from modules.patent.models import ReportSchedule
    
    schedule = ReportSchedule.objects.create(
        application=sample_application,
        scheduled_for=date(2024, 12, 31),
        created_by=principal.user_id,
    )
    return schedule


class TestReportGeneration:
    """Test cases for report generation functionality."""

    def test_report_budget_generation(self, principal, sample_application, sample_budget):
        """TEST-CFR-022-1 | PMS-AFR-183 | Verification of generating financial/budget reports (PCC_ADMIN/Director)."""
        
        # Test with PCC_ADMIN role
        response = principal.api_client.post(
            '/patent/reports/budget/',
            data={'application_id': sample_application.id},
            format='json'
        )
        
        assert response.status_code == 201, "Budget report should be generated successfully."
        assert 'budget_report' in response.data or 'report' in response.data

    def test_report_deadline_generation(self, principal, sample_application):
        """TEST-CFR-022-2 | PMS-AFR-184 | Verification of generating deadline/pending action reports (PCC_ADMIN/Director)."""
        
        # Test with PCC_ADMIN role
        response = principal.api_client.post(
            '/patent/reports/deadline/',
            data={'application_id': sample_application.id},
            format='json'
        )
        
        assert response.status_code == 201, "Deadline report should be generated successfully."
        assert 'deadline_report' in response.data or 'report' in response.data

    def test_report_inventor_generation(self, principal, sample_application, sample_inventor):
        """TEST-CFR-022-3 | PMS-AFR-185 | Verification of generating inventor/co-inventor reports (PCC_ADMIN/Director)."""
        
        # Test with PCC_ADMIN role
        response = principal.api_client.post(
            '/patent/reports/inventor/',
            data={'application_id': sample_application.id},
            format='json'
        )
        
        assert response.status_code == 201, "Inventor report should be generated successfully."
        assert 'inventor_report' in response.data or 'report' in response.data

    def test_report_portfolio_analysis(self, principal, sample_application):
        """TEST-CFR-022-4 | PMS-AFR-186 | Verification of generating patent portfolio analysis reports (PCC_ADMIN/Director)."""
        
        # Test with PCC_ADMIN role
        response = principal.api_client.post(
            '/patent/reports/portfolio/',
            data={'application_id': sample_application.id},
            format='json'
        )
        
        assert response.status_code == 201, "Portfolio analysis report should be generated successfully."
        assert 'portfolio_report' in response.data or 'report' in response.data

    def test_report_workload_generation(self, principal, sample_application):
        """TEST-CFR-022-5 | PMS-AFR-187 | Verification of generating workload/assignment reports (PCC_ADMIN/Director)."""
        
        # Test with PCC_ADMIN role
        response = principal.api_client.post(
            '/patent/reports/workload/',
            data={'application_id': sample_application.id},
            format='json'
        )
        
        assert response.status_code == 201, "Workload report should be generated successfully."
        assert 'workload_report' in response.data or 'report' in response.data

    def test_report_scheduling(self, principal, sample_application):
        """TEST-CFR-022-6 | PMS-AFR-188 | Verification of scheduling reports (authorized users)."""
        
        # Test with PCC_ADMIN role
        future_date = date.today() + timedelta(days=30)
        
        response = principal.api_client.post(
            '/patent/reports/schedule/',
            data={
                'application_id': sample_application.id,
                'scheduled_for': str(future_date),
                'report_type': 'budget',
            },
            format='json'
        )
        
        assert response.status_code == 201, "Report schedule should be created successfully."
        assert 'schedule' in response.data or 'id' in response.data

    def test_report_export(self, principal, sample_application):
        """TEST-CFR-022-7 | PMS-AFR-189 | Verification of exporting reports (authorized users)."""
        
        # Test with PCC_ADMIN role
        response = principal.api_client.post(
            '/patent/reports/export/',
            data={'application_id': sample_application.id, 'format': 'pdf'},
            format='json'
        )
        
        assert response.status_code == 200, "Report export should be available."
        assert 'export_url' in response.data or 'download' in response.data

    def test_report_customization(self, principal, sample_application):
        """TEST-CFR-022-8 | PMS-AFR-190 | Verification of customizing reports (authorized users)."""
        
        # Test with PCC_ADMIN role
        response = principal.api_client.post(
            '/patent/reports/customize/',
            data={
                'application_id': sample_application.id,
                'filters': {'status': 'approved'},
                'parameters': {'include_inventors': True},
            },
            format='json'
        )
        
        assert response.status_code == 200, "Report customization should be applied."
        assert 'customized_report' in response.data or 'report' in response.data


class TestDirectorRoleReports:
    """Test cases for report generation with Director role."""

    def test_budget_report_director(self, director_principal, sample_application, sample_budget):
        """TEST-CFR-022-1 | PMS-AFR-183 | Verification of generating financial/budget reports (Director)."""
        
        response = director_principal.api_client.post(
            '/patent/reports/budget/',
            data={'application_id': sample_application.id},
            format='json'
        )
        
        assert response.status_code == 201, "Budget report should be generated successfully by Director."

    def test_deadline_report_director(self, director_principal, sample_application):
        """TEST-CFR-022-2 | PMS-AFR-184 | Verification of generating deadline/pending action reports (Director)."""
        
        response = director_principal.api_client.post(
            '/patent/reports/deadline/',
            data={'application_id': sample_application.id},
            format='json'
        )
        
        assert response.status_code == 201, "Deadline report should be generated successfully by Director."

    def test_inventor_report_director(self, director_principal, sample_application, sample_inventor):
        """TEST-CFR-022-3 | PMS-AFR-185 | Verification of generating inventor/co-inventor reports (Director)."""
        
        response = director_principal.api_client.post(
            '/patent/reports/inventor/',
            data={'application_id': sample_application.id},
            format='json'
        )
        
        assert response.status_code == 201, "Inventor report should be generated successfully by Director."

    def test_portfolio_report_director(self, director_principal, sample_application):
        """TEST-CFR-022-4 | PMS-AFR-186 | Verification of generating patent portfolio analysis reports (Director)."""
        
        response = director_principal.api_client.post(
            '/patent/reports/portfolio/',
            data={'application_id': sample_application.id},
            format='json'
        )
        
        assert response.status_code == 201, "Portfolio analysis report should be generated successfully by Director."

    def test_workload_report_director(self, director_principal, sample_application):
        """TEST-CFR-022-5 | PMS-AFR-187 | Verification of generating workload/assignment reports (Director)."""
        
        response = director_principal.api_client.post(
            '/patent/reports/workload/',
            data={'application_id': sample_application.id},
            format='json'
        )
        
        assert response.status_code == 201, "Workload report should be generated successfully by Director."

    def test_scheduled_report_director(self, director_principal, sample_application):
        """TEST-CFR-022-6 | PMS-AFR-188 | Verification of scheduling reports (Director)."""
        
        future_date = date.today() + timedelta(days=30)
        
        response = director_principal.api_client.post(
            '/patent/reports/schedule/',
            data={
                'application_id': sample_application.id,
                'scheduled_for': str(future_date),
                'report_type': 'deadline',
            },
            format='json'
        )
        
        assert response.status_code == 201, "Report schedule should be created successfully by Director."

    def test_export_report_director(self, director_principal, sample_application):
        """TEST-CFR-022-7 | PMS-AFR-189 | Verification of exporting reports (Director)."""
        
        response = director_principal.api_client.post(
            '/patent/reports/export/',
            data={'application_id': sample_application.id, 'format': 'pdf'},
            format='json'
        )
        
        assert response.status_code == 200, "Report export should be available for Director."

    def test_custom_report_director(self, director_principal, sample_application):
        """TEST-CFR-022-8 | PMS-AFR-190 | Verification of customizing reports (Director)."""
        
        response = director_principal.api_client.post(
            '/patent/reports/customize/',
            data={
                'application_id': sample_application.id,
                'filters': {'status': 'approved'},
                'parameters': {'include_inventors': True},
            },
            format='json'
        )
        
        assert response.status_code == 200, "Report customization should be applied for Director."
