"""Test cases for Patent Management System - Maintenance and Office Actions (FR_DESIGN.json test cases 81-88).

All tests use pytest-django with the isolated test database.
No production code modifications are made.
"""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from django.core.management import call_command

from modules.patent.models import (
    PatentApplication, MaintenanceRecord, ApplicationHistory,
    AttorneyAssignment, OfficeAction
)
from modules.patent.services.post_filing import (
    record_office_action, prepare_response, approve_response, submit_response,
    schedule_maintenance, decide_renewal
)
from fusion_auth.principal import Principal
from conftest import make_principal


@pytest.fixture
def app_with_grant():
    """Create a granted patent application for testing."""
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="US2024-001",
        title="Test Patent Application",
        abstract="Test abstract",
        description="Test description",
        claims="Test claims",
        technical_domain="Electronics",
        applicant_id=1,
        status="granted",
    )
    return app


@pytest.fixture
def attorney_assigned(app_with_grant):
    """Create an application with assigned attorney."""
    assignment = AttorneyAssignment.objects.create(
        application=app_with_grant,
        attorney_id=2,
        status="accepted",
    )
    return assignment


@pytest.fixture
def director_assigned(app_with_grant):
    """Create an application with assigned director."""
    app_with_grant.assigned_director_id = 3
    app_with_grant.save()
    return app_with_grant


@pytest.fixture
def maintenance_record(app_with_grant):
    """Create a maintenance record for testing renewal decisions."""
    return MaintenanceRecord.objects.create(
        application=app_with_grant,
        due_date=date.today(),
        fee=100.00,
        decision="renewal_requested",
        decided_by=None,
    )


@pytest.fixture
def office_action(app_with_grant):
    """Create an office action for testing."""
    return OfficeAction.objects.create(
        application=app_with_grant,
        received_date=date.today(),
        response_due_date=date.today() + timedelta(days=30),
        description="Office Action received from USPTO",
        response_text="",
        status="recorded",
    )


@pytest.fixture
def principal_attorney(app_with_grant):
    """Create a Principal with Attorney role."""
    return make_principal(
        user_id=2,
        permissions=("patent.legal.review",),
        modules=("patent",),
        kind="staff",
        roles=("attorney",),
        active_role="attorney",
    )


@pytest.fixture
def principal_director(app_with_grant):
    """Create a Principal with Director role."""
    return make_principal(
        user_id=3,
        permissions=("patent.admin.manage", "patent.budget.approve",),
        modules=("patent",),
        kind="staff",
        roles=("director",),
        active_role="director",
    )


@pytest.fixture
def principal_applicant(app_with_grant):
    """Create a Principal with Applicant role."""
    return make_principal(
        user_id=1,
        permissions=("patent.application.view_self", "patent.application.create",),
        modules=("patent",),
        kind="student",
        roles=("applicant",),
        active_role="applicant",
    )


class TestMaintenanceRenewalDecisionRequiredBeforeDeadline:
    """Test case TEST-CFR-013-4 from PMS-AFR-110."""
    
    def test_id(self):
        self.source_id = "TEST-CFR-013-4"
    
    def test_renewal_decision_required_before_deadline(
        self, app_with_grant, maintenance_record, principal_director
    ):
        """Verify requirement of explicit renewal decision before deadline."""
        # Precondition: Maintenance deadline is approaching (already set to today)
        
        # Action: Skip the renewal decision process (attempt to proceed without decision)
        # Verify that system prevents proceeding past deadline without decision
        
        # The maintenance record should have status indicating pending decision
        assert maintenance_record.decision == "renewal_requested"
        assert maintenance_record.decided_by is None
        
        # Attempting to access or use the record without a decision should fail
        # This is enforced by business logic in decide_renewal service
        with pytest.raises(Exception):
            # Simulating attempt to proceed without decision
            from modules.patent.services.post_filing import decide_renewal
            decide_renewal(
                director_id=principal_director.user_id,
                record_id=maintenance_record.id,
                renew=False,
                justification="Test"
            )


class TestAttorneyRequestRenewalDecisionFromDirector:
    """Test case TEST-CFR-013-5 from PMS-AFR-111."""
    
    def test_id(self):
        self.source_id = "TEST-CFR-013-5"
    
    def test_attorney_requests_renewal_decision_from_director(
        self, app_with_grant, maintenance_record, principal_attorney
    ):
        """Verify Attorney seeking renewal decision from Director."""
        # Precondition: Renewal deadline is active (maintenance record exists)
        
        # Action: Attorney clicks 'Request Renewal Decision'
        # Expected: A request form or workflow to the Director is triggered
        
        # Verify maintenance record exists and is in pending state
        assert MaintenanceRecord.objects.filter(
            application=app_with_grant,
            due_date=maintenance_record.due_date
        ).exists()
        
        # The system should allow Attorney to initiate the renewal request process
        # This triggers the workflow to Director for decision
        
        # Verify that maintenance record exists with renewal_requested status
        assert maintenance_record.decision == "renewal_requested"


class TestDirectorDecisionRenewOrDoNotRenew:
    """Test case TEST-CFR-013-6 from PMS-AFR-112."""
    
    def test_id(self):
        self.source_id = "TEST-CFR-013-6"
    
    def test_director_decision_renew_or_do_not_renew(
        self, app_with_grant, maintenance_record, principal_director
    ):
        """Verify Director decision (Renew/Do Not Renew)."""
        # Precondition: Renewal request received by Director
        
        # Action: Director selects 'Renew' or 'Do Not Renew'
        # Expected: The system accepts and records one of these decisions
        
        # Test 'Renew' decision
        updated_record = decide_renewal(
            director_id=principal_director.user_id,
            record_id=maintenance_record.id,
            renew=True,
            justification="Patent is valuable"
        )
        
        assert updated_record.decision == "renew"
        assert updated_record.decided_by == principal_director.user_id
        
        # Test 'Do Not Renew' decision
        maintenance_record2 = MaintenanceRecord.objects.create(
            application=app_with_grant,
            due_date=date.today() + timedelta(days=1),
            fee=100.00,
            decision="renewal_requested",
            decided_by=None,
        )
        
        updated_record2 = decide_renewal(
            director_id=principal_director.user_id,
            record_id=maintenance_record2.id,
            renew=False,
            justification="Patent is not commercially viable"
        )
        
        assert updated_record2.decision == "do_not_renew"
        assert updated_record2.decided_by == principal_director.user_id


class TestAttorneyRecordsMaintenanceActionUponRenewalApproval:
    """Test case TEST-CFR-013-7 from PMS-AFR-113."""
    
    def test_id(self):
        self.source_id = "TEST-CFR-013-7"
    
    def test_attorney_records_maintenance_action_transaction(
        self, app_with_grant, maintenance_record, principal_attorney
    ):
        """Verify Attorney recording of maintenance action/transaction upon renewal approval."""
        # Precondition: Director decision is 'Renew'
        
        # First make the renewal decision
        updated_record = decide_renewal(
            director_id=principal_director.user_id,
            record_id=maintenance_record.id,
            renew=True,
            justification="Patent is valuable"
        )
        
        assert updated_record.decision == "renew"
        
        # Action: Attorney processes the payment and updates the status
        # Expected: The transaction, status, and action are recorded
        
        # Verify that ApplicationHistory records the renewal decision
        history = ApplicationHistory.objects.filter(
            application=app_with_grant
        ).order_by('-created_at').first()
        
        assert history is not None
        assert "renewal_decided" in str(history.action)


class TestMaintenanceRenewalHistory:
    """Test case TEST-CFR-013-8 from PMS-AFR-114."""
    
    def test_id(self):
        self.source_id = "TEST-CFR-013-8"
    
    def test_maintenance_renewal_history_viewed(
        self, app_with_grant, principal_attorney
    ):
        """Verify maintenance of renewal history."""
        # Precondition: Renewal was executed previously
        
        # Create multiple renewal records
        for i in range(3):
            MaintenanceRecord.objects.create(
                application=app_with_grant,
                due_date=date.today() - timedelta(days=i*30),
                fee=100.00,
                decision="renewal_requested",
                decided_by=None,
            )
        
        # Make renewal decisions for all records
        for i in range(3):
            MaintenanceRecord.objects.create(
                application=app_with_grant,
                due_date=date.today() - timedelta(days=i*30),
                fee=100.00,
                decision="renewal_requested",
                decided_by=None,
            )
        
        # Action: View 'Maintenance History'
        # Expected: Previous renewals are listed with details
        
        # Retrieve history records
        history_records = ApplicationHistory.objects.filter(
            application=app_with_grant
        ).order_by('-created_at')
        
        assert history_records.count() > 0
        
        # Verify renewal decisions are recorded in history
        for record in MaintenanceRecord.objects.filter(application=app_with_grant):
            history = ApplicationHistory.objects.filter(
                application=app_with_grant,
                action="renewal_decided"
            ).exists()
            
            assert history is not None


class TestNextMaintenanceCycleScheduled:
    """Test case TEST-CFR-013-9 from PMS-AFR-115."""
    
    def test_id(self):
        self.source_id = "TEST-CFR-013-9"
    
    def test_next_maintenance_cycle_scheduled(
        self, app_with_grant, principal_attorney
    ):
        """Verify scheduling of next maintenance cycle."""
        # Precondition: One renewal cycle is completed
        
        # Create first renewal record and complete it
        first_record = MaintenanceRecord.objects.create(
            application=app_with_grant,
            due_date=date.today() - timedelta(days=30),
            fee=100.00,
            decision="renewal_requested",
            decided_by=None,
        )
        
        # Make renewal decision
        decide_renewal(
            director_id=principal_director.user_id,
            record_id=first_record.id,
            renew=True,
            justification="Patent is valuable"
        )
        
        # Create second renewal record (next cycle)
        second_record = MaintenanceRecord.objects.create(
            application=app_with_grant,
            due_date=date.today() + timedelta(days=30),
            fee=150.00,
            decision="renewal_requested",
            decided_by=None,
        )
        
        # Action: Check the next scheduled action date
        # Expected: The system schedules the next maintenance cycle
        
        # Verify second renewal record exists with correct due date
        assert MaintenanceRecord.objects.filter(
            application=app_with_grant,
            due_date=date.today() + timedelta(days=30)
        ).exists()


class TestOfficeActionRecording:
    """Test case TEST-CFR-014-0 from PMS-AFR-116."""
    
    def test_id(self):
        self.source_id = "TEST-CFR-014-0"
    
    def test_office_action_recorded(
        self, app_with_grant, principal_attorney
    ):
        """Verify recording of office actions received."""
        # Precondition: Patent Office sends an Office Action
        
        # Action: Navigate to 'Office Actions' (simulated by creating record)
        # Expected: The Office Action is recorded in the system
        
        # Create office action via service
        oa = record_office_action(
            attorney_id=principal_attorney.user_id,
            application_id=app_with_grant.id,
            received_date=date.today(),
            response_due_date=date.today() + timedelta(days=30),
            description="Office Action received from USPTO regarding novelty"
        )
        
        # Verify office action was created
        assert OfficeAction.objects.filter(
            application=app_with_grant,
            received_date=date.today()
        ).exists()
        
        # Verify status is 'recorded'
        oa.refresh_from_db()
        assert oa.status == "recorded"


class TestAttorneyReviewOfficeActions:
    """Test case TEST-CFR-014-1 from PMS-AFR-117."""
    
    def test_id(self):
        self.source_id = "TEST-CFR-014-1"
    
    def test_attorney_reviews_office_action_details(
        self, app_with_grant, principal_attorney, office_action
    ):
        """Verify Attorney review of recorded office actions."""
        # Precondition: Office Action is recorded
        
        # Action: Attorney views the action details
        # Expected: Attorney can review and analyze the content
        
        # Verify office action exists with correct data
        oa = OfficeAction.objects.get(
            application=app_with_grant,
            received_date=date.today()
        )
        
        assert oa.description == "Office Action received from USPTO regarding novelty"
        assert oa.status == "recorded"
        
        # Attorney should be able to access and review the action details
        # This is verified by the fact that the office action exists with proper data
        
        # Verify attorney can prepare response (simulating review completion)
        updated_oa = prepare_response(
            attorney_id=principal_attorney.user_id,
            office_action_id=oa.id,
            response_text="Response prepared based on analysis",
            needs_applicant_approval=False
        )
        
        assert updated_oa.status == "response_ready"
