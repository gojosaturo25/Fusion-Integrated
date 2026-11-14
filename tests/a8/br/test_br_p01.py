"""
Automated backend tests for BR-PMS business rules (BR-PMS-003 through BR-PMS-020).
Generated from BR_DESIGN.json test specifications.
"""

import pytest
from datetime import date, timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.response import Response

from fusion_auth.client import IamSession
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument, AttorneyAssignment,
    PatentabilityOpinion, Budget, Filing, OfficeAction, ApplicationHistory
)
from modules.patent.domain.policy import (
    validate_document, missing_required_fields, can_withdraw
)


# -----------------------------------------------------------------------------
# Test Fixtures and Setup Helpers
# -----------------------------------------------------------------------------

@pytest.fixture
def api_client():
    """Create a DRF API client for testing."""
    return APIClient()


@pytest.fixture
def app_a(applicant_id=1001):
    """Create application owned by User A (Applicant role)."""
    from modules.patent.models import PatentApplication
    
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-001",
        applicant_id=applicant_id,
        title="Test Application A",
        abstract="Test abstract for application A",
        description="Test description for application A",
        claims="Test claims for application A",
        technical_domain="Technology X",
        status="submitted"
    )
    
    # Create inventor with agreement signed
    Inventor.objects.create(
        application=app,
        user_id=applicant_id,
        name="Inventor A",
        email="inventor_a@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def app_b(applicant_id=1002):
    """Create application owned by User B (Applicant role)."""
    from modules.patent.models import PatentApplication
    
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-002",
        applicant_id=applicant_id,
        title="Test Application B",
        abstract="Test abstract for application B",
        description="Test description for application B",
        claims="Test claims for application B",
        technical_domain="Technology Y",
        status="submitted"
    )
    
    # Create inventor with agreement signed
    Inventor.objects.create(
        application=app,
        user_id=applicant_id,
        name="Inventor B",
        email="inventor_b@test.com",
        contribution_percent=50.0,
        agreement_signed=True
    )
    
    return app


@pytest.fixture
def director_d(applicant_id=1003):
    """Create Director D with assigned domain."""
    from modules.patent.models import PatentApplication
    
    # Create application for Director D's domain
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-003",
        applicant_id=1001,
        title="Test Application C",
        abstract="Test abstract for application C",
        description="Test description for application C",
        claims="Test claims for application C",
        technical_domain="Technology Z",
        status="under_review",
        assigned_director_id=applicant_id
    )
    
    return app


@pytest.fixture
def workflow_b(applicant_id=1004):
    """Create application in Workflow B (different from Director D's domain)."""
    from modules.patent.models import PatentApplication
    
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-004",
        applicant_id=1001,
        title="Test Application D",
        abstract="Test abstract for application D",
        description="Test description for application D",
        claims="Test claims for application D",
        technical_domain="Technology W",
        status="submitted",
        assigned_director_id=applicant_id
    )
    
    return app


@pytest.fixture
def incomplete_app(applicant_id=1005):
    """Create application with missing required fields."""
    from modules.patent.models import PatentApplication
    
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-005",
        applicant_id=applicant_id,
        title="",  # Missing title
        abstract="",  # Missing abstract
        description="Test description for incomplete application",
        claims="Test claims for incomplete application",
        technical_domain="Technology V",
        status="submitted"
    )
    
    return app


@pytest.fixture
def pending_agreement_app(applicant_id=1006):
    """Create application with inventor agreement not signed."""
    from modules.patent.models import PatentApplication, Inventor
    
    app = PatentApplication.objects.create(
        APPLICATION_NUMBER="APP-2024-006",
        applicant_id=applicant_id,
        title="Test Application E",
        abstract="Test abstract for application E",
        description="Test description for application E",
        claims="Test claims for application E",
        technical_domain="Technology U",
        status="under_review"
    )
    
    # Create inventor with agreement NOT signed
    Inventor.objects.create(
        application=app,
        user_id=applicant_id,
        name="Inventor E",
        email="inventor_e@test.com",
        contribution_percent=50.0,
        agreement_signed=False  # Not signed
    )
    
    return app


# -----------------------------------------------------------------------------
# Test Cases from BR_DESIGN.json
# -----------------------------------------------------------------------------

class TestBRPMS003ApplicantAccessControl:
    """Test BR-PMS-003: Verify Applicant can only access their own application reports."""
    
    test_id = "BR-PMS-003"
    source_id = "BR-PMS-003"
    
    def test_applicant_cannot_view_others_application(self, app_a, app_b, api_client):
        """
        Purpose: Verify Applicant can only access their own application reports.
        
        Preconditions: Two users created in PMS with roles: User A as 'Applicant', 
                      User B as 'Applicant'. Two applications created: App1 belongs to 
                      User A, App2 belongs to User B. Reports generated for both apps.
        
        Action: User B attempts to view/report on App1 (owned by User A).
        
        Expected Result: Access denied; user is redirected to App2 or receives an error 
                        indicating lack of permission.
        """
        # Login as User B (Applicant role)
        from fusion_auth.principal import Principal
        
        session = IamSession(
            user_id=1002,
            username="u1002",
            display_name="User 1002",
            kind="student",
            active_role="student",
            roles=("student",),
            permissions=frozenset(["patent.application.view_self"]),
            modules=("patent",)
        )
        
        principal = Principal.from_session(session)
        
        # Set the principal on the request
        api_client.force_authenticate(user=principal.user_id)
        
        # Try to access App1 (owned by User A, applicant_id=1001)
        response = api_client.get(f'/patent/applications/{app_a.id}/')
        
        # Verify access is denied - should get 403 or similar error
        assert response.status_code == 403, "Applicant B should not be able to view App1"


class TestBRPMS005DirectorScopeRestriction:
    """Test BR-PMS-005: Verify Director can only access reports within their authorized scope."""
    
    test_id = "BR-PMS-005"
    source_id = "BR-PMS-005"
    
    def test_director_cannot_view_outside_domain_report(self, director_d, app_b, api_client):
        """
        Purpose: Verify Director can only access reports within their authorized scope.
        
        Preconditions: Director D assigned to Domain X. Report generated for Domain Y 
                      (different from D's scope). User logged in as Director D.
        
        Action: Director D attempts to view the report for Domain Y.
        
        Expected Result: Access denied; report is hidden or unavailable.
        """
        # Login as Director D
        session = IamSession(
            user_id=1003,
            username="u1003",
            display_name="Director D",
            kind="staff",
            active_role="director",
            roles=("director",),
            permissions=frozenset(["patent.application.review"]),
            modules=("patent",)
        )
        
        principal = Principal.from_session(session)
        
        # Set the principal on the request
        api_client.force_authenticate(user=principal.user_id)
        
        # Try to access App2 (belongs to User B, different domain from Director D's scope)
        response = api_client.get(f'/patent/applications/{app_b.id}/')
        
        # Verify access is denied - should get 403 or similar error
        assert response.status_code == 403, "Director D should not be able to view App2"


class TestBRPMS006DirectorWorkflowOversight:
    """Test BR-PMS-006: Verify Director workflow oversight access is limited to their domain workflows."""
    
    test_id = "BR-PMS-006"
    source_id = "BR-PMS-006"
    
    def test_director_cannot_override_status_outside_domain(self, director_d, workflow_b, api_client):
        """
        Purpose: Verify Director workflow oversight access is limited to their domain workflows.
        
        Preconditions: Director D assigned only to Workflow A. User logged in as Director D.
        
        Action: User attempts to access or override status in Workflow B (not in D's domain).
        
        Expected Result: Access denied; action blocked.
        """
        # Login as Director D
        session = IamSession(
            user_id=1003,
            username="u1003",
            display_name="Director D",
            kind="staff",
            active_role="director",
            roles=("director",),
            permissions=frozenset(["patent.application.review"]),
            modules=("patent",)
        )
        
        principal = Principal.from_session(session)
        
        # Set the principal on the request
        api_client.force_authenticate(user=principal.user_id)
        
        # Try to update status in Workflow B (different from Director D's domain)
        response = api_client.put(
            f'/patent/applications/{workflow_b.id}/',
            data={'status': 'approved'},
            format='json'
        )
        
        # Verify action is blocked - should get 403 or similar error
        assert response.status_code == 403, "Director D should not be able to override status outside their domain"


class TestBRPMS014PDFDocumentValidation:
    """Test BR-PMS-014: Verify PMS rejects non-PDF document uploads."""
    
    test_id = "BR-PMS-014"
    source_id = "BR-PMS-014"
    
    def test_non_pdf_document_rejected(self, incomplete_app, api_client):
        """
        Purpose: Verify PMS rejects non-PDF document uploads.
        
        Preconditions: Applicant attempting to upload application supporting documents 
                      via the submission interface.
        
        Action: User attempts to upload a Word (.docx) file as a required document.
        
        Expected Result: Validation fails; system prompts user to convert/upload PDF only.
        """
        # Login as applicant
        session = IamSession(
            user_id=1005,
            username="u1005",
            display_name="User 1005",
            kind="student",
            active_role="student",
            roles=("student",),
            permissions=frozenset(["patent.application.create"]),
            modules=("patent",)
        )
        
        principal = Principal.from_session(session)
        
        # Set the principal on the request
        api_client.force_authenticate(user=principal.user_id)
        
        # Try to submit application with non-PDF document
        response = api_client.post(
            '/patent/submit/',
            data={
                'applicant_id': 1005,
                'title': "Test Application",
                'abstract': "Test abstract",
                'description': "Test description",
                'claims': "Test claims",
                'technical_domain': "Technology",
                'inventors': [],
                'documents': [
                    {
                        'file_name': "test.docx",  # Non-PDF file
                        'content_type': "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        'size': 1024
                    }
                ]
            },
            format='json'
        )
        
        # Verify validation fails - should get error about invalid documents
        assert response.status_code == 400, "Non-PDF document should be rejected"


class TestBRPMS015DocumentSizeLimit:
    """Test BR-PMS-015: Verify PMS rejects documents exceeding 50 MB."""
    
    test_id = "BR-PMS-015"
    source_id = "BR-PMS-015"
    
    def test_document_exceeding_50mb_rejected(self, incomplete_app, api_client):
        """
        Purpose: Verify PMS rejects documents exceeding 50 MB.
        
        Preconditions: Valid PDF file created; Upload interface open.
        
        Action: User attempts to upload a document exactly 51 MB in size.
        
        Expected Result: Validation fails; system returns error message stating limit is 50 MB.
        """
        # Login as applicant
        session = IamSession(
            user_id=1005,
            username="u1005",
            display_name="User 1005",
            kind="student",
            active_role="student",
            roles=("student",),
            permissions=frozenset(["patent.application.create"]),
            modules=("patent",)
        )
        
        principal = Principal.from_session(session)
        
        # Set the principal on the request
        api_client.force_authenticate(user=principal.user_id)
        
        # Try to submit application with document exceeding 50 MB (51 MB = 52428800 bytes)
        response = api_client.post(
            '/patent/submit/',
            data={
                'applicant_id': 1005,
                'title': "Test Application",
                'abstract': "Test abstract",
                'description': "Test description",
                'claims': "Test claims",
                'technical_domain': "Technology",
                'inventors': [],
                'documents': [
                    {
                        'file_name': "test.pdf",  # PDF file
                        'content_type': "application/pdf",
                        'size': 52428801  # 51 MB in bytes
                    }
                ]
            },
            format='json'
        )
        
        # Verify validation fails - should get error about document size limit
        assert response.status_code == 400, "Document exceeding 50 MB should be rejected"


class TestBRPMS016MalwareScanValidation:
    """Test BR-PMS-016: Verify PMS rejects documents failing malware scan."""
    
    test_id = "BR-PMS-016"
    source_id = "BR-PMS-016"
    
    def test_malware_document_rejected(self, incomplete_app, api_client):
        """
        Purpose: Verify PMS rejects documents failing malware scan.
        
        Preconditions: Malware detected in a file by security service (mocked via test 
                      fixture or simulated flag).
        
        Action: User attempts to submit the malicious file alongside valid metadata.
        
        Expected Result: Submission rejected; system returns error regarding failed 
                       malware validation.
        """
        # Login as applicant
        session = IamSession(
            user_id=1005,
            username="u1005",
            display_name="User 1005",
            kind="student",
            active_role="student",
            roles=("student",),
            permissions=frozenset(["patent.application.create"]),
            modules=("patent",)
        )
        
        principal = Principal.from_session(session)
        
        # Set the principal on the request
        api_client.force_authenticate(user=principal.user_id)
        
        # Try to submit application with malware file (simulated via content_type flag)
        response = api_client.post(
            '/patent/submit/',
            data={
                'applicant_id': 1005,
                'title': "Test Application",
                'abstract': "Test abstract",
                'description': "Test description",
                'claims': "Test claims",
                'technical_domain': "Technology",
                'inventors': [],
                'documents': [
                    {
                        'file_name': "malicious.pdf",  # PDF file (simulated malware)
                        'content_type': "application/pdf",
                        'size': 1024,
                        'is_malware': True  # Simulate malware detection
                    }
                ]
            },
            format='json'
        )
        
        # Verify submission is rejected - should get error about malware validation
        assert response.status_code == 400, "Malware document should be rejected"


class TestBRPMS017RequiredFieldValidation:
    """Test BR-PMS-017: Verify PMS rejects incomplete application submissions."""
    
    test_id = "BR-PMS-017"
    source_id = "BR-PMS-017"
    
    def test_incomplete_application_rejected(self, incomplete_app, api_client):
        """
        Purpose: Verify PMS rejects incomplete application submissions.
        
        Preconditions: Application form open; Some required fields (e.g., Title, Abstract) 
                      left empty.
        
        Action: User attempts to submit the application without filling all mandatory 
                fields.
        
        Expected Result: Submission rejected; system highlights missing required fields 
                       and prevents acceptance.
        """
        # Login as applicant
        session = IamSession(
            user_id=1005,
            username="u1005",
            display_name="User 1005",
            kind="student",
            active_role="student",
            roles=("student",),
            permissions=frozenset(["patent.application.create"]),
            modules=("patent",)
        )
        
        principal = Principal.from_session(session)
        
        # Set the principal on the request
        api_client.force_authenticate(user=principal.user_id)
        
        # Try to submit application with missing required fields
        response = api_client.post(
            '/patent/submit/',
            data={
                'applicant_id': 1005,
                'title': "",  # Missing title
                'abstract': "",  # Missing abstract
                'description': "Test description",
                'claims': "Test claims",
                'technical_domain': "Technology",
                'inventors': [],
                'documents': []
            },
            format='json'
        )
        
        # Verify submission is rejected - should get error about missing fields
        assert response.status_code == 400, "Incomplete application should be rejected"


class TestBRPMS020ExternalFilingBeforeAgreement:
    """Test BR-PMS-020: Verify PMS prevents external filing before agreement completion."""
    
    test_id = "BR-PMS-020"
    source_id = "BR-PMS-020"
    
    def test_external_filing_blocked_before_agreement(self, pending_agreement_app, api_client):
        """
        Purpose: Verify PMS prevents external filing before agreement completion.
        
        Preconditions: Application status is 'Under Review' or similar; Inventor 
                      Agreements status is 'Pending/Incomplete'.
        
        Action: Attorney attempts to initiate 'External Filing' action.
        
        Expected Result: Action blocked; system returns error stating Inventor 
                       agreements are not complete.
        """
        # Login as attorney (simulated)
        session = IamSession(
            user_id=1006,
            username="u1006",
            display_name="Attorney 1006",
            kind="staff",
            active_role="attorney",
            roles=("attorney",),
            permissions=frozenset(["patent.legal.review"]),
            modules=("patent",)
        )
        
        principal = Principal.from_session(session)
        
        # Set the principal on the request
        api_client.force_authenticate(user=principal.user_id)
        
        # Try to record filing for application with pending agreement
        response = api_client.post(
            f'/patent/filings/{pending_agreement_app.id}/',
            data={
                'office': "USPTO",
                'filing_number': "123456789",
                'filing_date': date.today(),
                'international': False
            },
            format='json'
        )
        
        # Verify action is blocked - should get error about incomplete agreements
        assert response.status_code == 400, "External filing should be blocked before agreement completion"


# -----------------------------------------------------------------------------
# Test Execution
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
