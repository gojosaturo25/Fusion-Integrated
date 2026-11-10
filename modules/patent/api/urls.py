from django.urls import path
from rest_framework.views import APIView

from .views import (
    ApplicationListView, ApplicationDetailView, ApplicationHistoryView,
    SubmitApplicationView, AssignDirectorView, ReviewApplicationView,
    ResubmitApplicationView, WithdrawApplicationView, FileAppealView,
    DecideAppealView, ExpireOverdueResubmissionsView, AdminApplicationListView
)
from .views_legal import (
    AssignAttorneyView, RespondToAssignmentView, MyAttorneyAssignmentsView,
    RecordOpinionView, ProposeBudgetView, DecideBudgetView, RecordFilingView,
    RecordOfficeActionView, PrepareResponseView, ApproveResponseView, SubmitResponseView,
    RecordGrantView, ScheduleMaintenanceView, DecideRenewalView
)

urlpatterns = [
    # --- Application Routes ---
    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('history/', ApplicationHistoryView.as_view(), name='application-history'),

    # --- Action Routes ---
    path('submit/', SubmitApplicationView.as_view(), name='submit-application'),
    path('assign-director/', AssignDirectorView.as_view(), name='assign-director'),
    path('review/', ReviewApplicationView.as_view(), name='review-application'),
    path('resubmit/', ResubmitApplicationView.as_view(), name='resubmit-application'),
    path('withdraw/', WithdrawApplicationView.as_view(), name='withdraw-application'),
    path('appeal/', FileAppealView.as_view(), name='file-appeal'),
    path('appeals/<int:pk>/', DecideAppealView.as_view(), name='decide-appeal'),

    # --- Admin Routes ---
    path('admin/applications/', AdminApplicationListView.as_view(), name='admin-application-list'),
    path('admin/expire-resubmissions/', ExpireOverdueResubmissionsView.as_view(), name='admin-expire-resubmissions'),

    # --- Legal Service Routes ---
    path('assign-attorney/', AssignAttorneyView.as_view(), name='assign-attorney'),
    path('assignments/<int:pk>/', RespondToAssignmentView.as_view(), name='respond-to-assignment'),
    path('my-assignments/', MyAttorneyAssignmentsView.as_view(), name='my-attorney-assignments'),
    path('opinions/<int:pk>/', RecordOpinionView.as_view(), name='record-opinion'),
    path('budgets/<int:pk>/', ProposeBudgetView.as_view(), name='propose-budget'),
    path('budgets/<int:pk>/decide/', DecideBudgetView.as_view(), name='decide-budget'),
    path('filings/<int:pk>/', RecordFilingView.as_view(), name='record-filing'),
    path('office-actions/<int:pk>/', RecordOfficeActionView.as_view(), name='record-office-action'),
    path('office-actions/<int:pk>/response/', PrepareResponseView.as_view(), name='prepare-response'),
    path('office-actions/<int:pk>/response/approve/', ApproveResponseView.as_view(), name='approve-response'),
    path('office-actions/<int:pk>/response/submit/', SubmitResponseView.as_view(), name='submit-response'),
    path('applications/<int:pk>/grant/', RecordGrantView.as_view(), name='record-grant'),
    path('maintenance/<int:pk>/', ScheduleMaintenanceView.as_view(), name='schedule-maintenance'),
    path('maintenance/<int:pk>/decide/', DecideRenewalView.as_view(), name='decide-renewal'),
]
