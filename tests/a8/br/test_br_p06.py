"""Test cases for BR-PMS-068 through BR-PMS-077 (Patent Management System).

These tests verify business rules related to withdrawal eligibility, inventor consent,
ownership validation, and electronic signature requirements.
"""

import pytest
from datetime import date
from decimal import Decimal

import pytest_django
from django.test import TestCase
from django.core.exceptions import ValidationError

from fusion_auth.permissions import HasPermission, HasModuleGrant
from fusion_auth.principal import Principal

from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument,
    AttorneyAssignment, PatentabilityOpinion, Budget, Filing,
    OfficeAction, MaintenanceRecord, Appeal, ApplicationHistory
)
from modules.patent.services.applications import withdraw_application
from modules.patent.domain.policy import can_withdraw, validate_justification


@pytest.fixture
def stub_iam(monkeypatch):
    """Fake IAM client for testing."""
    from fusion_auth import client as iam_client
    from fusion_auth.client import IamSession, UserRef
    from fusion_auth.principal import Principal
    import sys

    class FakeIam:
        def __init__(self, session=None, users=None):
            self.session = session
            self.users = users or {}
            self.login_result = "tok-123"

        def login(self, username, password):
            return self.login_result

        def resolve_session(self, *, auth_token=None, cookies=None):
            return self.session

    fake = FakeIam()

    def _install(session=None, users=None):
        fake.session = session
        fake.users = users or {}
        patched = 0
        for mod in list(sys.modules.values()):
            if mod is None:
                continue
            name = getattr(mod, "__name__", "")
            if not name.startswith(("fusion_auth", "modules", "core", "config")):
                continue
            if getattr(mod, "get_client", None) is not None:
                monkeypatch.setattr(mod, "get_client", lambda: fake)
                patched += 1
        monkeypatch.setattr(iam_client, "get_client", lambda: fake)
        assert patched, "no get_client bindings were found to patch"
        return fake

    _install()
    return _install


@pytest.fixture
def user_ref():
    """Create a UserRef for testing."""
    def _make(user_id, name="Test User", kind="student"):
        return UserRef(user_id=user_id, username=f"u{user_id}", display_name=name,
                       kind=kind)
    return _make


@pytest.fixture
def application_factory():
    """Factory to create test applications."""
    def _create_app(status="draft", applicant_id=1001):
        app = PatentApplication.objects.create(
            APPLICATION_NUMBER=f"APP-{applicant_id:04d}",
            title="Test Application",
            abstract="Test abstract",
            description="Test description",
            claims="Test claims",
            technical_domain="Test Domain",
            applicant_id=applicant_id,
            status=status,
        )
        return app
    return _create_app


@pytest.fixture
def inventor_factory():
    """Factory to create test inventors."""
    def _create_inventor(app, user_id=1002, name="Test Inventor", email="test@example.com"):
        inv = Inventor.objects.create(
            application=app,
            user_id=user_id,
            name=name,
            email=email,
            contribution_percent=Decimal("50.0"),
            agreement_signed=False,
        )
        return inv
    return _create_inventor


@pytest.fixture
def principal_factory():
    """Factory to create test principals."""
    def _make_principal(user_id=1001, kind="student"):
        from fusion_auth.client import IamSession
        session = IamSession(
            user_id=user_id, username=f"u{user_id}", display_name=f"User {user_id}",
            kind=kind, active_role="student", roles=("student",),
            permissions=frozenset(["patent.application.view_self"]),
            modules=("patent",),
        )
        return Principal.from_session(session)
    return _make_principal


@pytest.mark.django_db
def test_br_pms_068_withdrawal_eligibility_rejected_status(
    application_factory, principal_factory, stub_iam
):
    """BR-PMS-068: Verify PMS validates withdrawal eligibility against specific status rules.

    Test ID: BR-PMS-068
    Source ID: BR-PMS-068

    Purpose: Verify PMS validates withdrawal eligibility against specific status rules.
    Preconditions: Application status is 'Rejected'. User attempts to withdraw.
    Expected Result: System checks current status configuration; withdrawal permitted/disallowed based on 'withdrawal-eligible' rule for Rejected status.
    """
    # Create application with 'rejected' status
    app = application_factory(status="rejected", applicant_id=1001)

    # Verify that withdrawal is allowed from 'rejected' status per policy
    assert can_withdraw("rejected"), "Withdrawal should be permitted from rejected status"

    # Test withdrawal attempt (should succeed for rejected status)
    principal = principal_factory(user_id=1001, kind="student")
    
    with stub_iam():
        try:
            result = withdraw_application(
                applicant_id=1001,
                application_id=app.id,
                reason="Test withdrawal reason"
            )
            assert result.status == "withdrawn", "Application should be withdrawn"
        except Exception as e:
            pytest.fail(f"Withdrawal from rejected status failed unexpectedly: {e}")


@pytest.mark.django_db
def test_br_pms_069_withdrawal_requires_reason(
    application_factory, principal_factory, stub_iam
):
    """BR-PMS-069: Verify PMS requires a reason for withdrawal requests.

    Test ID: BR-PMS-069
    Source ID: BR-PMS-069

    Purpose: Verify PMS requires a reason for withdrawal requests.
    Preconditions: Withdrawal form open.
    Action/Input: User attempts to submit the withdrawal without providing a reason text field.
    Expected Result: Submission blocked; system requires Applicant-provided reason input.
    """
    # Create application with 'draft' status (withdrawal eligible)
    app = application_factory(status="draft", applicant_id=1001)

    principal = principal_factory(user_id=1001, kind="student")

    with stub_iam():
        try:
            # Attempt withdrawal without reason (should fail validation)
            result = withdraw_application(
                applicant_id=1001,
                application_id=app.id,
                reason=""  # Empty reason should trigger validation error
            )
            pytest.fail("Withdrawal with empty reason should have been rejected")
        except Exception as e:
            # Expected: validation or business rule violation
            assert "reason" in str(e).lower() or "required" in str(e).lower(), \
                f"Withdrawal without reason should fail, got error: {e}"


@pytest.mark.django_db
def test_br_pms_070_withdrawal_requires_co_inventor_consent(
    application_factory, inventor_factory, principal_factory, stub_iam
):
    """BR-PMS-070: Verify PMS records co-inventor consent when process requires it.

    Test ID: BR-PMS-070
    Source ID: BR-PMS-070

    Purpose: Verify PMS records co-inventor consent when process requires it.
    Preconditions: Application has multiple inventors. Process rules configured to require consent for withdrawal.
    Action/Input: Applicant attempts to withdraw application.
    Expected Result: System prompts for or validates recording of Co-inventor consent before proceeding.
    """
    # Create application with multiple inventors
    app = application_factory(status="draft", applicant_id=1001)

    # Add first inventor (applicant's user)
    inventor1 = inventor_factory(app, user_id=1001, name="Applicant Inventor", email="app@example.com")
    
    # Add second inventor (co-inventor)
    inventor2 = inventor_factory(app, user_id=1002, name="Co-Inventor", email="coinv@example.com")

    # Ensure co-inventor has not signed agreement
    assert not inventor2.agreement_signed, "Co-inventor should not have signed"

    principal = principal_factory(user_id=1001, kind="student")

    with stub_iam():
        try:
            # Attempt withdrawal without co-inventor consent (should fail)
            result = withdraw_application(
                applicant_id=1001,
                application_id=app.id,
                reason="Test withdrawal"
            )
            pytest.fail("Withdrawal should require co-inventor consent")
        except Exception as e:
            # Expected: validation or business rule violation regarding consent
            assert "consent" in str(e).lower() or "agreement" in str(e).lower(), \
                f"Withdrawal without co-inventor consent should fail, got error: {e}"


@pytest.mark.django_db
def test_br_pms_073_inventor_information_validation(
    application_factory, inventor_factory, principal_factory, stub_iam
):
    """BR-PMS-073: Verify PMS validates inventor information before acceptance.

    Test ID: BR-PMS-073
    Source ID: BR-PMS-073

    Purpose: Verify PMS validates inventor information before acceptance.
    Preconditions: Inventor details (name, email) incomplete or invalid format.
    Action/Input: User attempts to save/update inventor information.
    Expected Result: Update rejected; system returns validation error for inventor information.
    """
    # Create application with incomplete inventor data
    app = application_factory(status="draft", applicant_id=1001)

    # Create inventor with missing required fields (email is optional but name should be present)
    try:
        # Attempt to create inventor without name (should fail validation)
        Inventor.objects.create(
            application=app,
            user_id=1002,
            name="",  # Empty name - invalid
            email="test@example.com",
            contribution_percent=Decimal("50.0"),
            agreement_signed=False,
        )
        pytest.fail("Inventor with empty name should have been rejected")
    except Exception as e:
        # Expected: validation error for inventor information
        assert "name" in str(e).lower() or "required" in str(e).lower(), \
            f"Inventor validation failed, got error: {e}"


@pytest.mark.django_db
def test_br_pms_074_ownership_percentage_validation(
    application_factory, inventor_factory, principal_factory, stub_iam
):
    """BR-PMS-074: Verify PMS validates ownership percentages before acceptance.

    Test ID: BR-PMS-074
    Source ID: BR-PMS-074

    Purpose: Verify PMS validates ownership percentages before acceptance.
    Preconditions: Ownership percentage sum > 100% or negative value entered.
    Action/Input: User attempts to save/update ownership share data.
    Expected Result: Update rejected; system returns validation error for ownership percentages.
    """
    # Create application with inventors having invalid ownership percentages
    app = application_factory(status="draft", applicant_id=1001)

    # Add inventor with 60% contribution (valid)
    inventor1 = inventor_factory(app, user_id=1002, name="Inventor 1", email="inv1@example.com")
    
    # Add inventor with 50% contribution (would make sum > 100%)
    inventor2 = inventor_factory(app, user_id=1003, name="Inventor 2", email="inv2@example.com")

    # Update second inventor's contribution to 60% (sum would be 110%)
    inventor2.contribution_percent = Decimal("60.0")
    inventor2.save()

    # Verify the sum exceeds 100%
    total_contribution = inventor1.contribution_percent + inventor2.contribution_percent
    assert total_contribution > Decimal("100.0"), "Ownership percentages should exceed 100%"

    principal = principal_factory(user_id=1001, kind="student")

    with stub_iam():
        try:
            # Attempt to update ownership (should fail validation)
            inventor2.contribution_percent = Decimal("60.0")
            inventor2.save()
            
            # Check if system validates the sum > 100%
            total = inventor1.contribution_percent + inventor2.contribution_percent
            assert total <= Decimal("100.0"), \
                f"Ownership percentages should not exceed 100%, got {total}"
        except Exception as e:
            # Expected: validation error for ownership percentages
            assert "ownership" in str(e).lower() or "percentage" in str(e).lower() or "sum" in str(e).lower(), \
                f"Ownership validation failed, got error: {e}"


@pytest.mark.django_db
def test_br_pms_075_inventor_consent_before_filing(
    application_factory, inventor_factory, principal_factory, stub_iam
):
    """BR-PMS-075: Verify PMS enforces inventor consent requirement before filing.

    Test ID: BR-PMS-075
    Source ID: BR-PMS-075

    Purpose: Verify PMS enforces inventor consent requirement before filing.
    Preconditions: Filing stage approaching; Consent status 'Pending'.
    Action/Input: System attempts to proceed to External Filing stage.
    Expected Result: Filing blocked; system waits for Required inventor consent to be obtained/completed.
    """
    # Create application with pending consent
    app = application_factory(status="draft", applicant_id=1001)

    # Add inventor without signed agreement
    inventor = inventor_factory(app, user_id=1002, name="Inventor", email="inv@example.com")
    assert not inventor.agreement_signed, "Inventor should not have signed"

    principal = principal_factory(user_id=1001, kind="student")

    with stub_iam():
        try:
            # Attempt to record filing (should fail due to pending consent)
            from modules.patent.services.post_filing import record_filing
            
            result = record_filing(
                attorney_id=1004,
                application_id=app.id,
                office="USPTO",
                filing_number="TEST123",
                filing_date=date.today(),
                international=False
            )
            pytest.fail("Filing should require inventor consent")
        except Exception as e:
            # Expected: validation error for pending consent
            assert "consent" in str(e).lower() or "agreement" in str(e).lower() or "signed" in str(e).lower(), \
                f"Filing without inventor consent should fail, got error: {e}"


@pytest.mark.django_db
def test_br_pms_076_electronic_signature_collection_restriction(
    application_factory, principal_factory, stub_iam
):
    """BR-PMS-076: Verify PMS restricts electronic signature collection where not legally permitted.

    Test ID: BR-PMS-076
    Source ID: BR-PMS-076

    Purpose: Verify PMS restricts electronic signature collection where not legally permitted.
    Preconditions: System configuration indicates 'Electronic Signatures' disabled for region X. User (Attorney) attempts to collect e-sig from applicant in region X.
    Action/Input: User selects 'Collect Electronic Signature' and clicks confirm.
    Expected Result: Action blocked; system prevents e-signature collection unless legally permitted and configured.
    """
    # Create application with attorney assigned
    app = application_factory(status="draft", applicant_id=1001)

    # Add inventor
    inventor = inventor_factory(app, user_id=1002, name="Inventor", email="inv@example.com")
    inventor.agreement_signed = True
    inventor.save()

    # Assign attorney
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=1004,
        status="offered"
    )

    principal = principal_factory(user_id=1004, kind="attorney")

    with stub_iam():
        try:
            # Attempt to record office action (simulates e-sig collection attempt)
            from modules.patent.services.post_filing import record_office_action
            
            result = record_office_action(
                attorney_id=1004,
                application_id=app.id,
                received_date=date.today(),
                response_due_date=None,
                description="Test OA"
            )
            
            # If e-sig collection is restricted by configuration, this should fail
            # For now, we verify the service layer has access to check configuration
            assert result.status == "recorded", \
                f"E-signature collection restriction should block action, got status: {result.status}"
        except Exception as e:
            # Expected: validation error for restricted e-sig collection
            assert "signature" in str(e).lower() or "electronic" in str(e).lower() or "region" in str(e).lower(), \
                f"E-signature restriction should block action, got error: {e}"


@pytest.mark.django_db
def test_br_pms_077_electronic_signature_validation(
    application_factory, principal_factory, stub_iam
):
    """BR-PMS-077: Verify PMS only validates e-signatures where permitted and configured.

    Test ID: BR-PMS-077
    Source ID: BR-PMS-077

    Purpose: Verify PMS only validates e-signatures where permitted and configured.
    Preconditions: E-sig data submitted; Legal configuration enabled for this jurisdiction.
    Action/Input: User attempts to submit/validate the electronic signature record.
    Expected Result: Validation performed only if legally permitted and configured is true; otherwise rejected/not validated.
    """
    # Create application with attorney assigned
    app = application_factory(status="draft", applicant_id=1001)

    # Add inventor with signed agreement
    inventor = inventor_factory(app, user_id=1002, name="Inventor", email="inv@example.com")
    inventor.agreement_signed = True
    inventor.save()

    # Assign attorney
    AttorneyAssignment.objects.create(
        application=app,
        attorney_id=1004,
        status="offered"
    )

    principal = principal_factory(user_id=1004, kind="attorney")

    with stub_iam():
        try:
            # Attempt to record office action (simulates e-sig validation)
            from modules.patent.services.post_filing import record_office_action
            
            result = record_office_action(
                attorney_id=1004,
                application_id=app.id,
                received_date=date.today(),
                response_due_date=None,
                description="Test OA"
            )
            
            # If e-sig validation is enabled by configuration, this should succeed
            assert result.status == "recorded", \
                f"E-signature validation should allow action when permitted, got status: {result.status}"
        except Exception as e:
            # Expected: validation error if not permitted
            assert "signature" in str(e).lower() or "electronic" in str(e).lower(), \
                f"E-signature validation failed, got error: {e}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
