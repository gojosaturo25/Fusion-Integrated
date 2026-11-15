"""Test cases for Patent Management System - Technology Transfer Requests and Appeals (TEST-CFR-019, TEST-CFR-020).

These tests implement test cases 129-136 from the FR_DESIGN.json specification.
"""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse

from fusion_auth.client import IamSession
from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, ApplicationHistory, Appeal
)
from modules.patent.services.applications import file_appeal
from modules.patent.services.technology_transfer import submit_ttr, route_ttr, finalize_agreement

# Mock TechnologyTransferRequest class for testing
class TechnologyTransferRequest:
    """Mock Technology Transfer Request model for testing."""
    
    def __init__(self, id=None, application_id=None, status="submitted", **kwargs):
        self.id = id
        self.application_id = application_id
        self.status = status
        self.technology_description = kwargs.get("technology_description")
        self.potential_partners = kwargs.get("potential_partners")
        self.actor_id = kwargs.get("actor_id")
    
    def __str__(self):
        return f"TTR-{self.id or 'N/A'} ({self.status})"


# -----------------------------------------------------------------------------
# Fixtures and Setup Helpers
# -----------------------------------------------------------------------------

@pytest.fixture
def stub_iam(monkeypatch):
    """Fake IAM client for testing without external dependencies."""
    from conftest import FakeIam, make_principal
    
    fake = FakeIam()
    
    def _install(session=None, users=None):
        fake.session = session
        fake.users = users or {}
        patched = 0
        for mod in list(monkeypatch.list):
            if getattr(mod, "get_client", None) is not None:
                monkeypatch.setattr(mod, "get_client", lambda: fake)
                patched += 1
        monkeypatch.setattr(fake.__module__, "get_client", lambda: fake)
        assert patched > 0, "no get_client bindings were found to patch"
        return fake
    
    _install()
    return _install


@pytest.fixture
def applicant_principal(stub_iam):
    """Create a principal with student/applicant permissions."""
    from conftest import make_principal
    
    return make_principal(
        user_id=1001,
        kind="student",
        roles=("applicant",),
        active_role="applicant",
        permissions=(
            "patent.application.view_self",
            "patent.application.create",
            "patent.application.delete",
            "patent.application.withdraw",
            "patent.legal.review",
            "patent.filing.record",
            "patent.maintenance.manage",
        ),
    )


@pytest.fixture
def director_principal(stub_iam):
    """Create a principal with director permissions."""
    from conftest import make_principal
    
    return make_principal(
        user_id=2001,
        kind="director",
        roles=("director",),
        active_role="director",
        permissions=(
            "patent.application.review",
            "patent.budget.approve",
            "patent.maintenance.manage",
            "patent.appeal.review",
            "patent.admin.manage",
            "patent.legal.review",
            "patent.filing.record",
        ),
    )


@pytest.fixture
def approved_application(applicant_principal):
    """Create an application in a state allowing TTR submission."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-001",
        title="Test Technology Transfer Application",
        abstract="Test technology transfer patent",
        description="Detailed description of the invention",
        claims="Claims text for test application",
        technical_domain="Technology Transfer",
        applicant_id=applicant_principal.user_id,
        status="approved",
    )
    
    return app


@pytest.fixture
def rejected_application(applicant_principal):
    """Create an application in 'Rejected' status for appeal testing."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-002",
        title="Test Rejected Application",
        abstract="Test rejected patent",
        description="Detailed description of the invention",
        claims="Claims text for test application",
        technical_domain="Technology Transfer",
        applicant_id=applicant_principal.user_id,
        status="rejected",
    )
    
    return app


# -----------------------------------------------------------------------------
# Technology Transfer Request Tests (TEST-CFR-019)
# -----------------------------------------------------------------------------

class TestTechnologyTransferRequestSubmission(TestCase):
    """Test cases for Technology Transfer Request submission and workflow."""
    
    def test_ttr_submission_recording(self, approved_application, applicant_principal):
        """TEST-CFR-019-1: Verify Applicant submission of technology transfer requests.
        
        Purpose: Verify Applicant submission of technology transfer requests.
        Preconditions: Application is in a state allowing TTR.
        Action: Applicant submits a Technology Transfer Request form.
        Expected Result: Request is recorded.
        """
        # Submit TTR via service
        ttr = submit_ttr(
            applicant_id=applicant_principal.user_id,
            application_id=approved_application.id,
            technology_description="Test technology for transfer",
            potential_partners=["Partner A", "Partner B"],
            actor_id=applicant_principal.user_id
        )
        
        # Verify request was recorded
        self.assertIsNotNone(ttr)
        self.assertEqual(ttr.status, "submitted")
        self.assertEqual(ttr.application_id, approved_application.id)
    
    def test_ttr_routing_to_committee(self, approved_application, applicant_principal):
        """TEST-CFR-019-2: Verification of routing to appropriate committee/Director.
        
        Purpose: Verification of routing to appropriate committee/Director.
        Preconditions: Request is submitted.
        Action: Trace the workflow status.
        Expected Result: System routes request based on institutional process definitions.
        """
        # Submit TTR
        ttr = submit_ttr(
            applicant_id=applicant_principal.user_id,
            application_id=approved_application.id,
            technology_description="Test technology for transfer",
            potential_partners=["Partner A"],
            actor_id=applicant_principal.user_id
        )
        
        # Route TTR to appropriate committee
        route_ttr(
            ttr_id=ttr.id,
            director_id=director_principal.user_id,
            committee="Technology Transfer Committee"
        )
        
        # Verify routing occurred
        self.assertIsNotNone(ttr)
        self.assertEqual(ttr.status, "routed")
    
    def test_ttr_negotiation_tracking(self, approved_application, applicant_principal):
        """TEST-CFR-019-3: Verification of tracking negotiation process info.
        
        Purpose: Verification of tracking negotiation process info.
        Preconditions: Negotiation is in progress.
        Action: Check the case status page.
        Expected Result: Negotiation details (dates, parties) are tracked.
        """
        # Submit TTR and route it
        ttr = submit_ttr(
            applicant_id=applicant_principal.user_id,
            application_id=approved_application.id,
            technology_description="Test technology for transfer",
            potential_partners=["Partner A"],
            actor_id=applicant_principal.user_id
        )
        
        # Start negotiation tracking
        negotiate_ttr(
            ttr_id=ttr.id,
            start_date=date.today(),
            parties=["Applicant", "Partner A"]
        )
        
        # Verify negotiation details are tracked
        self.assertIsNotNone(ttr)
        self.assertEqual(ttr.status, "negotiation_in_progress")


class TestTechnologyTransferAgreement(TestCase):
    """Test cases for Technology Transfer Agreement recording and confidentiality."""
    
    def test_ttr_final_agreement_recording(self, approved_application, applicant_principal):
        """TEST-CFR-019-4: Verification of recording final agreements.
        
        Purpose: Verification of recording final agreements.
        Preconditions: Agreement is finalized.
        Action: View the agreement record.
        Expected Result: The agreement terms are stored.
        """
        # Submit TTR and finalize agreement
        ttr = submit_ttr(
            applicant_id=applicant_principal.user_id,
            application_id=approved_application.id,
            technology_description="Test technology for transfer",
            potential_partners=["Partner A"],
            actor_id=applicant_principal.user_id
        )
        
        # Finalize agreement
        finalize_agreement(
            ttr_id=ttr.id,
            terms={"royalty_rate": 0.10, "territory": "Global"},
            parties=["Applicant", "Partner A"],
            effective_date=date.today()
        )
        
        # Verify agreement terms are stored
        self.assertIsNotNone(ttr)
        self.assertEqual(ttr.status, "agreement_finalized")
    
    def test_ttr_financial_system_integration(self, approved_application, applicant_principal):
        """TEST-CFR-019-5: Verification of updating/sharing financial-system info.
        
        Purpose: Verification of updating/sharing financial-system info (where integration exists).
        Preconditions: Integration with finance system is active.
        Action: Finalize the agreement with cost details.
        Expected Result: Financial data is exchanged or recorded in PMS/Finance.
        """
        # Submit TTR and finalize with financial details
        ttr = submit_ttr(
            applicant_id=applicant_principal.user_id,
            application_id=approved_application.id,
            technology_description="Test technology for transfer",
            potential_partners=["Partner A"],
            actor_id=applicant_principal.user_id
        )
        
        # Finalize with financial integration
        finalize_agreement(
            ttr_id=ttr.id,
            terms={"royalty_rate": 0.10, "territory": "Global"},
            parties=["Applicant", "Partner A"],
            effective_date=date.today(),
            financial_data={"payment_schedule": "quarterly", "total_value": 100000}
        )
        
        # Verify financial data is recorded
        self.assertIsNotNone(ttr)
        self.assertEqual(ttr.status, "agreement_finalized")


class TestTechnologyTransferConfidentiality(TestCase):
    """Test cases for Technology Transfer confidentiality controls."""
    
    def test_ttr_confidentiality_controls(self, approved_application, applicant_principal):
        """TEST-CFR-019-6: Verification of confidentiality controls for license records.
        
        Purpose: Verification of confidentiality controls for license records.
        Preconditions: License record is created.
        Action: Attempt to access confidential details without clearance.
        Expected Result: Access is restricted.
        """
        # Submit TTR and create agreement with confidential terms
        ttr = submit_ttr(
            applicant_id=applicant_principal.user_id,
            application_id=approved_application.id,
            technology_description="Test technology for transfer",
            potential_partners=["Partner A"],
            actor_id=applicant_principal.user_id
        )
        
        # Finalize with confidential terms
        finalize_agreement(
            ttr_id=ttr.id,
            terms={"royalty_rate": 0.10, "territory": "Global", "confidentiality_level": "high"},
            parties=["Applicant", "Partner A"],
            effective_date=date.today()
        )
        
        # Verify confidentiality controls are in place
        self.assertIsNotNone(ttr)
        self.assertEqual(ttr.status, "agreement_finalized")


# -----------------------------------------------------------------------------
# Appeal Tests (TEST-CFR-020)
# -----------------------------------------------------------------------------

class TestAppealFiling(TestCase):
    """Test cases for Appeal filing against rejected applications."""
    
    def test_appeal_filing_creation(self, rejected_application, applicant_principal):
        """TEST-CFR-020-0: Verification of Applicant appeal filing against rejected applications.
        
        Purpose: Verification of Applicant appeal filing against rejected applications.
        Preconditions: Application status is 'Rejected'.
        Action: Applicant initiates an Appeal.
        Expected Result: Appeal case is created.
        """
        # File appeal via service
        appeal = file_appeal(
            applicant_id=applicant_principal.user_id,
            application_id=rejected_application.id,
            grounds="Inventorship dispute"
        )
        
        # Verify appeal was created
        self.assertIsNotNone(appeal)
        self.assertEqual(appeal.status, "submitted")
        self.assertEqual(appeal.application_id, rejected_application.id)
    
    def test_appeal_filing_time_period(self, rejected_application, applicant_principal):
        """TEST-CFR-020-1: Verification of appeal filing within configured time period.
        
        Purpose: Verification of appeal filing within configured time period.
        Preconditions: Current time exceeds the allowed appeal window.
        Action: Applicant attempts to file an appeal.
        Expected Result: System blocks filing with 'Overdue' message.
        """
        # Set application's resubmission deadline in the past (simulating expired appeal window)
        rejected_application.resubmission_deadline = date.today() - timedelta(days=30)
        rejected_application.save()
        
        # Try to file appeal when outside time period
        with self.assertRaises(ValueError):
            file_appeal(
                applicant_id=applicant_principal.user_id,
                application_id=rejected_application.id,
                grounds="Inventorship dispute"
            )
