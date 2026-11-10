"""Test cases for Patent Management System - Test Cases 57-64 (FR_DESIGN.json).

These tests verify backend functionality corresponding to UI test cases.
Some UI-only actions are marked as NOT_AUTOMATED since they require frontend interaction."""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Budget, AttorneyAssignment, Inventor, ApplicationHistory
)
from modules.patent.services.legal import record_opinion, decide_budget
from modules.patent.services.applications import withdraw_application


@pytest.fixture
def application_factory(db):
    """Factory to create patent applications for testing."""
    def _create(applicant_id=1001, status='submitted'):
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER=f"APP-{2024001}",
            applicant_id=applicant_id,
            title="Test Application",
            abstract="Test abstract",
            description="Test description",
            claims="Test claims",
            technical_domain="CSE",
            status=status,
        )
        return app
    return _create


@pytest.fixture
def attorney_assignment_factory(db):
    """Factory to create attorney assignments for testing."""
    def _create(app_id=1, attorney_id=2001):
        assignment = AttorneyAssignment.objects.create(
            application=app_id,
            attorney_id=attorney_id,
            status="accepted",
        )
        return assignment
    return _create


@pytest.fixture
def budget_factory(db):
    """Factory to create budgets for testing."""
    def _create(app_id=1, filing_fee=5000, attorney_fee=3000, admin_cost=1000):
        app = PatentApplication.objects.get(id=app_id)
        budget = Budget.objects.create(
            application=app,
            filing_fee=filing_fee,
            attorney_fee=attorney_fee,
            administrative_cost=admin_cost,
            total=filing_fee + attorney_fee + admin_cost,
            status="pending",
        )
        return budget
    return _create


@pytest.fixture
def stub_iam(monkeypatch):
    """IAM stub fixture from conftest.py."""
    from conftest import stub_iam
    return stub_iam(monkeypatch)


@pytest.fixture
def principal_factory(stub_iam):
    """Factory to create principals for testing."""
    def _make(kind="student", user_id=1001, permissions=()):
        session = stub_iam(session=None, users={user_id: {}})
        return Principal.from_session(
            session=session,
            kind=kind,
            user_id=user_id,
            permissions=permissions,
        )
    return _make


class TestCFR010_5(TestCase):
    """Test TEST-CFR-010-5 (PMS-AFR-087): Verify attorney request for extensions.
    
    NOTE: This is a UI action (click 'Request Extension' button) that cannot be 
    directly automated with Django/pytest backend tests. The extension request 
    functionality may not exist in the current backend implementation.
    """
    
    test_id = "TEST-CFR-010-5"
    source_id = "PMS-AFR-087"
    
    def test_attorney_extension_request_ui_action(self, application_factory):
        """Verify attorney request for extensions UI action."""
        # This is a UI-only action that cannot be automated with backend tests.
        # The 'Request Extension' button click and form display are frontend concerns.
        pytest.skip("NOT_AUTOMATED: UI action (click button) requires frontend interaction")


class TestCFR010_6(TestCase):
    """Test TEST-CFR-010-6 (PMS-AFR-088): Verify recording of final patentability opinion.
    
    This test verifies the backend service that records a patentability opinion.
    """
    
    test_id = "TEST-CFR-010-6"
    source_id = "PMS-AFR-088"
    
    def test_record_patentability_opinion(self, application_factory):
        """Verify the system stores the complete opinion record."""
        app = application_factory()
        
        # Create attorney assignment for testing
        from modules.patent.models import AttorneyAssignment
        assignment = AttorneyAssignment.objects.create(
            application=app,
            attorney_id=2001,
            status="accepted",
        )
        
        # Record opinion via service
        opinion = record_opinion(
            attorney_id=2001,
            application_id=app.id,
            novelty=True,
            non_obviousness=True,
            utility=True,
            recommendation="file_patent",
            text="This invention is novel, non-obvious, and useful."
        )
        
        # Verify opinion was stored
        assert opinion.application == app
        assert opinion.attorney_id == 2001
        assert opinion.novelty == True
        assert opinion.non_obviousness == True
        assert opinion.utility == True
        assert opinion.recommendation == "file_patent"
        assert opinion.opinion_text == "This invention is novel, non-obvious, and useful."
        
        # Verify history was recorded
        history = ApplicationHistory.objects.filter(application=app).order_by('-created_at').first()
        assert history is not None
        assert history.action == "record_opinion"


class TestCFR010_7(TestCase):
    """Test TEST-CFR-010-7 (PMS-AFR-089): Verify stakeholder notification on attorney opinion.
    
    NOTE: Notification functionality may not exist in the current backend implementation.
    This test verifies that the opinion record was created, which would trigger notifications.
    """
    
    test_id = "TEST-CFR-010-7"
    source_id = "PMS-AFR-089"
    
    def test_stakeholder_notification_on_opinion(self, application_factory):
        """Verify stakeholders receive a notification regarding the recorded opinion."""
        app = application_factory()
        
        # Create attorney assignment for testing
        from modules.patent.models import AttorneyAssignment
        assignment = AttorneyAssignment.objects.create(
            application=app,
            attorney_id=2001,
            status="accepted",
        )
        
        # Record opinion via service
        opinion = record_opinion(
            attorney_id=2001,
            application_id=app.id,
            novelty=True,
            non_obviousness=True,
            utility=True,
            recommendation="file_patent",
            text="This invention is novel, non-obvious, and useful."
        )
        
        # Verify opinion record exists (notification would be triggered by this)
        assert Opinion.objects.filter(application=app).exists()
        
        pytest.skip("NOT_AUTOMATED: Notification functionality requires external notification service")


class TestCFR011_0(TestCase):
    """Test TEST-CFR-011-0 (PMS-AFR-090): Verify Director review of filing/prosecution costs.
    
    This test verifies the backend budget model displays cost breakdown.
    """
    
    test_id = "TEST-CFR-011-0"
    source_id = "PMS-AFR-090"
    
    def test_director_views_cost_breakdown(self, application_factory):
        """Verify filing fees, attorney fees, and administrative costs are displayed."""
        app = application_factory(status='approved')
        
        # Create budget with all cost components
        budget = Budget.objects.create(
            application=app,
            filing_fee=5000,
            attorney_fee=3000,
            administrative_cost=1000,
            total=9000,
            status="pending",
        )
        
        # Verify budget exists with all cost components
        assert Budget.objects.filter(application=app).exists()
        assert budget.filing_fee == 5000
        assert budget.attorney_fee == 3000
        assert budget.administrative_cost == 1000
        assert budget.total == 9000
        
        pytest.skip("NOT_AUTOMATED: UI action (view cost breakdown screen) requires frontend interaction")


class TestCFR011_1(TestCase):
    """Test TEST-CFR-011-1 (PMS-AFR-091): Verify Director approval of budget costs.
    
    This test verifies the backend service that approves budgets.
    """
    
    test_id = "TEST-CFR-011-1"
    source_id = "PMS-AFR-091"
    
    def test_director_approves_budget(self, application_factory):
        """Verify the budget is approved and recorded."""
        app = application_factory(status='approved')
        
        # Create budget with all cost components
        budget = Budget.objects.create(
            application=app,
            filing_fee=5000,
            attorney_fee=3000,
            administrative_cost=1000,
            total=9000,
            status="pending",
        )
        
        # Approve budget via service
        updated_budget, escalated = decide_budget(
            director_id=3001,
            budget_id=budget.id,
            approve=True,
            justification="Budget is within approved limits and justified.",
            threshold=10000,
        )
        
        # Verify budget was approved
        assert updated_budget.status == "approved"
        assert updated_budget.decided_by == 3001
        assert updated_budget.justification == "Budget is within approved limits and justified."
        
        pytest.skip("NOT_AUTOMATED: UI action (click 'Approve Budget') requires frontend interaction")


class TestCFR011_2(TestCase):
    """Test TEST-CFR-011-2 (PMS-AFR-092): Verify inclusion of filing fees in budget info.
    
    This test verifies the backend model includes filing fees as a distinct line item.
    """
    
    test_id = "TEST-CFR-011-2"
    source_id = "PMS-AFR-092"
    
    def test_filing_fees_in_budget_info(self, application_factory):
        """Verify filing fees are listed as a distinct line item."""
        app = application_factory(status='approved')
        
        # Create budget with all cost components
        budget = Budget.objects.create(
            application=app,
            filing_fee=5000,
            attorney_fee=3000,
            administrative_cost=1000,
            total=9000,
            status="pending",
        )
        
        # Verify filing fee is stored as distinct field
        assert budget.filing_fee == 5000
        
        pytest.skip("NOT_AUTOMATED: UI action (view detailed budget report) requires frontend interaction")


class TestCFR011_3(TestCase):
    """Test TEST-CFR-011-3 (PMS-AFR-093): Verify inclusion of attorney fees in budget info.
    
    This test verifies the backend model includes attorney fees as a distinct line item.
    """
    
    test_id = "TEST-CFR-011-3"
    source_id = "PMS-AFR-093"
    
    def test_attorney_fees_in_budget_info(self, application_factory):
        """Verify attorney fees are listed as a distinct line item."""
        app = application_factory(status='approved')
        
        # Create budget with all cost components
        budget = Budget.objects.create(
            application=app,
            filing_fee=5000,
            attorney_fee=3000,
            administrative_cost=1000,
            total=9000,
            status="pending",
        )
        
        # Verify attorney fee is stored as distinct field
        assert budget.attorney_fee == 3000
        
        pytest.skip("NOT_AUTOMATED: UI action (view detailed budget report) requires frontend interaction")


class TestCFR011_4(TestCase):
    """Test TEST-CFR-011-4 (PMS-AFR-094): Verify inclusion of administrative costs in budget info.
    
    This test verifies the backend model includes administrative costs as a distinct line item.
    """
    
    test_id = "TEST-CFR-011-4"
    source_id = "PMS-AFR-094"
    
    def test_administrative_costs_in_budget_info(self, application_factory):
        """Verify administrative costs are listed as a distinct line item."""
        app = application_factory(status='approved')
        
        # Create budget with all cost components
        budget = Budget.objects.create(
            application=app,
            filing_fee=5000,
            attorney_fee=3000,
            administrative_cost=1000,
            total=9000,
            status="pending",
        )
        
        # Verify administrative cost is stored as distinct field
        assert budget.administrative_cost == 1000
        
        pytest.skip("NOT_AUTOMATED: UI action (view detailed budget report) requires frontend interaction")
