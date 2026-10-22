"""
URL patterns for the Leave Management API.
Maps HTTP methods and paths to DRF views.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from modules.leave.api.views import (
    ApplicationListCreateView,
    ApplicationDetailView,
    WithdrawView,
    CancelView,
    SubstituteResponseView,
    ReplaceSubstituteView,
    InboxView,
    DecideView,
    BalanceView,
    ReportingLineView,
)

# Router for generic CRUD if needed in future, though we use specific views here.
router = DefaultRouter()

urlpatterns = [
    # Application Management
    path("applications/", ApplicationListCreateView.as_view(), name="applications-list"),
    
    # Single Application Detail (used by all actions)
    path("applications/<int:pk>/", ApplicationDetailView.as_view(), name="application-detail"),
    
    # Lifecycle Actions on Application
    path("applications/<int:pk>/withdraw/", WithdrawView.as_view(), name="withdraw-application"),
    path("applications/<int:pk>/cancel/", CancelView.as_view(), name="cancel-approved-leave"),
    path("applications/<int:pk>/substitute-response/", SubstituteResponseView.as_view(), name="respond-to-substitute"),
    path("applications/<int:pk>/replace-substitute/", ReplaceSubstituteView.as_view(), name="replace-substitute"),
    
    # Decision Actions (Inbox and specific decisions)
    path("inbox/", InboxView.as_view(), name="approvals-inbox-list"),
    path("applications/<int:pk>/decide/", DecideView.as_view(), name="decide-application"),
    
    # Balances and History
    path("balances/<int:year>/", BalanceView.as_view(), name="user-balances"),
]
