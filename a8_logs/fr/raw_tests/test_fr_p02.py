"""Test cases for Patent Management System - Application Submission (CFR-005)."""
import pytest
from datetime import date
from io import BytesIO

import pytest_django
from django.core.files.base import ContentFile

from fusion_auth.principal import Principal
from modules.patent.models import (
    PatentApplication, Inventor, ApplicationDocument,
)
from modules.patent.domain.policy import validate_document, missing_required_fields


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-005-0 - Complete application submission by Applicant
# Source: PMS-AFR-038
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_cfr_005_0_complete_application_submission(
    stub_iam, user_ref, monkeypatch
):
    """Verify complete application submission by Applicant."""
    
    # Arrange
    applicant = user_ref(user_id=1001, kind="student")
    principal = Principal.from_session(applicant)
    
    # Create a valid application with all required fields
    data = {
        "title": "Test Patent Application",
        "abstract": "This is a test abstract.",
        "description": "Detailed description of the invention.",
        "claims": "The claims section of the patent application.",
        "technical_domain": "Computer Science"
    }
    
    inventors = [
        {"user_id": 1001, "name": "Test Inventor", "email": "inventor@test.com", 
         "contribution_percent": 50.0, "agreement_signed": True}
    ]
    
    documents = [
        {
            "file_name": "application_draft.pdf",
            "content_type": "application/pdf",
            "size": 1024 * 100  # ~100 KB
        }
    ]
    
    # Act - Submit application via service layer
    from modules.patent.services.applications import submit_application
    
    app = submit_application(
        applicant_id=applicant.user_id,
        data=data,
        inventors=inventors,
        documents=documents,
        actor_id=applicant.user_id
    )
    
    # Assert - Submission is accepted and application record is created
    assert app is not None
    assert app.status == "submitted"
    assert app.version_number == 1
    assert app.title == data["title"]
    assert len(app.inventors.all()) == 1
    assert len(app.documents.all()) == 1


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-005-1 - Rejection of non-PDF documents
# Source: PMS-AFR-039
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_cfr_005_1_rejection_of_non_pdf_documents(
    stub_iam, user_ref, monkeypatch
):
    """Verify rejection of non-PDF documents."""
    
    # Arrange
    applicant = user_ref(user_id=1002, kind="student")
    principal = Principal.from_session(applicant)
    
    data = {
        "title": "Test Patent Application",
        "abstract": "This is a test abstract.",
        "description": "Detailed description of the invention.",
        "claims": "The claims section of the patent application.",
        "technical_domain": "Computer Science"
    }
    
    inventors = [
        {"user_id": 1002, "name": "Test Inventor", "email": "inventor@test.com", 
         "contribution_percent": 50.0, "agreement_signed": True}
    ]
    
    # Create a non-PDF document (DOCX)
    doc_content = b"fake docx content"
    doc_data = {
        "file_name": "application_draft.docx",
        "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "size": len(doc_content)
    }
    
    # Act - Attempt to submit with non-PDF document
    from modules.patent.services.applications import submit_application
    
    with pytest.raises(ValueError) as exc_info:
        app = submit_application(
            applicant_id=applicant.user_id,
            data=data,
            inventors=inventors,
            documents=[doc_data],
            actor_id=applicant.user_id
        )
    
    # Assert - System rejects the document with error message
    assert "Invalid documents" in str(exc_info.value)
    assert "PDF" in str(exc_info.value).upper()


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-005-2 - Rejection of oversized documents (>50 MB)
# Source: PMS-AFR-040
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_cfr_005_2_rejection_of_oversized_documents(
    stub_iam, user_ref, monkeypatch
):
    """Verify rejection of oversized documents (>50 MB)."""
    
    # Arrange
    applicant = user_ref(user_id=1003, kind="student")
    principal = Principal.from_session(applicant)
    
    data = {
        "title": "Test Patent Application",
        "abstract": "This is a test abstract.",
        "description": "Detailed description of the invention.",
        "claims": "The claims section of the patent application.",
        "technical_domain": "Computer Science"
    }
    
    inventors = [
        {"user_id": 1003, "name": "Test Inventor", "email": "inventor@test.com", 
         "contribution_percent": 50.0, "agreement_signed": True}
    ]
    
    # Create a document that is 51 MB (exceeds 50 MB limit)
    doc_content = b"x" * (51 * 1024 * 1024)  # 51 MB
    doc_data = {
        "file_name": "large_application.pdf",
        "content_type": "application/pdf",
        "size": len(doc_content)
    }
    
    # Act - Attempt to submit with oversized document
    from modules.patent.services.applications import submit_application
    
    with pytest.raises(ValueError) as exc_info:
        app = submit_application(
            applicant_id=applicant.user_id,
            data=data,
            inventors=inventors,
            documents=[doc_data],
            actor_id=applicant.user_id
        )
    
    # Assert - System rejects the document with error message about exceeding 50 MB
    assert "Invalid documents" in str(exc_info.value)
    assert "50 MB" in str(exc_info.value).upper()


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-005-3 - Malware validation on submission
# Source: PMS-AFR-041
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_cfr_005_3_malware_validation_on_submission(
    stub_iam, user_ref, monkeypatch
):
    """Verify malware validation on submission."""
    
    # Arrange
    applicant = user_ref(user_id=1004, kind="student")
    principal = Principal.from_session(applicant)
    
    data = {
        "title": "Test Patent Application",
        "abstract": "This is a test abstract.",
        "description": "Detailed description of the invention.",
        "claims": "The claims section of the patent application.",
        "technical_domain": "Computer Science"
    }
    
    inventors = [
        {"user_id": 1004, "name": "Test Inventor", "email": "inventor@test.com", 
         "contribution_percent": 50.0, "agreement_signed": True}
    ]
    
    # Create a document with known malicious code (simulated)
    doc_content = b"fake malware content"
    doc_data = {
        "file_name": "malicious_application.pdf",
        "content_type": "application/pdf",
        "size": len(doc_content)
    }
    
    # Act - Attempt to submit with potentially malicious document
    from modules.patent.services.applications import submit_application
    
    # Note: Malware validation is assumed to be handled by external service or middleware
    # This test verifies the policy layer behavior for malware detection
    with pytest.raises(ValueError) as exc_info:
        app = submit_application(
            applicant_id=applicant.user_id,
            data=data,
            inventors=inventors,
            documents=[doc_data],
            actor_id=applicant.user_id
        )
    
    # Assert - System rejects the document with warning about malware/threats
    assert "Invalid documents" in str(exc_info.value) or "malware" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-005-4 - Rejection of incomplete application data
# Source: PMS-AFR-042
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_cfr_005_4_rejection_of_incomplete_application_data(
    stub_iam, user_ref, monkeypatch
):
    """Verify rejection of incomplete application data."""
    
    # Arrange
    applicant = user_ref(user_id=1005, kind="student")
    principal = Principal.from_session(applicant)
    
    # Submit application missing the 'Claims' section
    data = {
        "title": "Test Patent Application",
        "abstract": "This is a test abstract.",
        "description": "Detailed description of the invention.",
        # Missing 'claims' field
        "technical_domain": "Computer Science"
    }
    
    inventors = [
        {"user_id": 1005, "name": "Test Inventor", "email": "inventor@test.com", 
         "contribution_percent": 50.0, "agreement_signed": True}
    ]
    
    documents = [
        {
            "file_name": "application_draft.pdf",
            "content_type": "application/pdf",
            "size": 1024 * 100
        }
    ]
    
    # Act - Attempt to submit incomplete application
    from modules.patent.services.applications import submit_application
    
    with pytest.raises(ValueError) as exc_info:
        app = submit_application(
            applicant_id=applicant.user_id,
            data=data,
            inventors=inventors,
            documents=documents,
            actor_id=applicant.user_id
        )
    
    # Assert - System prevents submission with validation error listing missing required fields
    assert "Missing required fields" in str(exc_info.value)
    assert "claims" in str(exc_info.value).lower()


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-005-5 - Document sensitivity classification
# Source: PMS-AFR-043
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_cfr_005_5_document_sensitivity_classification(
    stub_iam, user_ref, monkeypatch
):
    """Verify document metadata displays classified sensitivity levels."""
    
    # Arrange
    applicant = user_ref(user_id=1006, kind="student")
    principal = Principal.from_session(applicant)
    
    data = {
        "title": "Test Patent Application",
        "abstract": "This is a test abstract.",
        "description": "Detailed description of the invention.",
        "claims": "The claims section of the patent application.",
        "technical_domain": "Computer Science"
    }
    
    inventors = [
        {"user_id": 1006, "name": "Test Inventor", "email": "inventor@test.com", 
         "contribution_percent": 50.0, "agreement_signed": True}
    ]
    
    documents = [
        {
            "file_name": "application_draft.pdf",
            "content_type": "application/pdf",
            "size": 1024 * 100
        }
    ]
    
    # Act - Submit application and retrieve metadata
    from modules.patent.services.applications import submit_application
    
    app = submit_application(
        applicant_id=applicant.user_id,
        data=data,
        inventors=inventors,
        documents=documents,
        actor_id=applicant.user_id
    )
    
    # Assert - Document metadata displays classified sensitivity levels
    assert app.documents.all().exists()
    doc = app.documents.first()
    assert doc.sensitivity in ["public", "internal", "confidential"]


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-005-6 - Unique Application ID assignment
# Source: PMS-AFR-044
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_cfr_005_6_unique_application_id_assignment(
    stub_iam, user_ref, monkeypatch
):
    """Verify unique alphanumeric Application ID is generated."""
    
    # Arrange
    applicant = user_ref(user_id=1007, kind="student")
    principal = Principal.from_session(applicant)
    
    data = {
        "title": "Test Patent Application",
        "abstract": "This is a test abstract.",
        "description": "Detailed description of the invention.",
        "claims": "The claims section of the patent application.",
        "technical_domain": "Computer Science"
    }
    
    inventors = [
        {"user_id": 1007, "name": "Test Inventor", "email": "inventor@test.com", 
         "contribution_percent": 50.0, "agreement_signed": True}
    ]
    
    documents = [
        {
            "file_name": "application_draft.pdf",
            "content_type": "application/pdf",
            "size": 1024 * 100
        }
    ]
    
    # Act - Submit application and retrieve created record
    from modules.patent.services.applications import submit_application
    
    app = submit_application(
        applicant_id=applicant.user_id,
        data=data,
        inventors=inventors,
        documents=documents,
        actor_id=applicant.user_id
    )
    
    # Assert - Unique alphanumeric Application ID is generated and displayed
    assert app.APPLICATION_NUMBER is not None
    assert len(app.APPLICATION_NUMBER) > 0
    assert str(app.APPLICATION_NUMBER).isalnum()


# -----------------------------------------------------------------------------
# Test Case: TEST-CFR-005-7 - Application status set to 'Submitted'
# Source: PMS-AFR-045
# -----------------------------------------------------------------------------

@pytest.mark.django_db
def test_cfr_005_7_application_status_set_to_submitted(
    stub_iam, user_ref, monkeypatch
):
    """Verify application status is updated to 'Submitted'."""
    
    # Arrange
    applicant = user_ref(user_id=1008, kind="student")
    principal = Principal.from_session(applicant)
    
    data = {
        "title": "Test Patent Application",
        "abstract": "This is a test abstract.",
        "description": "Detailed description of the invention.",
        "claims": "The claims section of the patent application.",
        "technical_domain": "Computer Science"
    }
    
    inventors = [
        {"user_id": 1008, "name": "Test Inventor", "email": "inventor@test.com", 
         "contribution_percent": 50.0, "agreement_signed": True}
    ]
    
    documents = [
        {
            "file_name": "application_draft.pdf",
            "content_type": "application/pdf",
            "size": 1024 * 100
        }
    ]
    
    # Act - Submit application and check status
    from modules.patent.services.applications import submit_application
    
    app = submit_application(
        applicant_id=applicant.user_id,
        data=data,
        inventors=inventors,
        documents=documents,
        actor_id=applicant.user_id
    )
    
    # Assert - Application status is updated to 'Submitted'
    assert app.status == "submitted"
