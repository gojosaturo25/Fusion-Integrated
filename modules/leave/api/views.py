"""Leave API views (rewritten in Phase 2)."""
from datetime import date
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.exceptions import NotFoundError
from fusion_auth.permissions import HasModuleGrant, HasPermission
from modules.leave import selectors
from modules.leave.api.serializers import (
    ApplySerializer, DecisionSerializer, LeaveApplicationSerializer, LeaveBalanceSerializer,
    ReplaceSubstituteSerializer, ReportingLineSerializer, SubstituteResponseSerializer,
)
from modules.leave.services import admin, applications, lifecycle


class ApplicationListCreateView(APIView):
    permission_classes = []

    def get_permissions(self):
        if self.request.method == "GET":
            return [HasPermission("leave.application.view_own")]
        elif self.request.method == "POST":
            return [HasPermission("leave.application.apply")]
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        user_id = request.principal.user_id
        apps = selectors.my_applications(user_id)
        serializer = LeaveApplicationSerializer(apps, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ApplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user_id = request.principal.user_id
        app = applications.apply_leave(user_id, data["kind"], data)
        return Response(LeaveApplicationSerializer(app).data, status=status.HTTP_201_CREATED)


class ApplicationDetailView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.view_own")]

    def get(self, request, application_id, *args, **kwargs):
        app = selectors.visible_application(request.principal.user_id, application_id)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class WithdrawView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.apply")]

    def post(self, request, application_id, *args, **kwargs):
        applications.withdraw(request.principal.user_id, application_id)
        app = selectors.visible_application(request.principal.user_id, application_id)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class CancelView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.apply")]

    def post(self, request, application_id, *args, **kwargs):
        today = timezone.localdate()
        lifecycle.request_cancellation(request.principal.user_id, application_id, today)
        app = selectors.visible_application(request.principal.user_id, application_id)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class SubstituteResponseView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.substitute.respond")]

    def post(self, request, application_id, *args, **kwargs):
        data = request.data
        accept = data.get("accept", False)
        lifecycle.respond_to_substitute(request.principal.user_id, application_id, accept)
        app = selectors.visible_application(request.principal.user_id, application_id)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class ReplaceSubstituteView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.apply")]

    def post(self, request, application_id, *args, **kwargs):
        data = request.data
        substitute_id = data["substitute_id"]
        lifecycle.replace_substitute(request.principal.user_id, application_id, substitute_id)
        app = selectors.visible_application(request.principal.user_id, application_id)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class InboxView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.review", "leave.substitute.respond")]

    def get(self, request, *args, **kwargs):
        user_id = request.principal.user_id
        apps = selectors.inbox(user_id)
        serializer = LeaveApplicationSerializer(apps, many=True)
        return Response(serializer.data)


class DecideView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.review", "leave.application.sanction")]

    def post(self, request, application_id, *args, **kwargs):
        data = request.data
        decision = data["decision"]
        remark = data.get("remark", "")

        app = selectors.visible_application(request.principal.user_id, application_id)

        if app.stage == "establishment":
            if not request.principal.has_permission("leave.application.verify"):
                raise NotFoundError("You do not have permission to decide at this stage.")
        elif app.stage == "sanction":
            if not request.principal.has_permission("leave.application.sanction"):
                raise NotFoundError("You do not have permission to decide at this stage.")

        lifecycle.decide(request.principal.user_id, application_id, decision, remark)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class BalanceView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.view_own")]

    def get(self, request, *args, **kwargs):
        user_id = request.principal.user_id
        year = int(request.query_params.get("year", timezone.now().year))
        kind = request.query_params.get("kind", "staff")
        balances = admin.ensure_balances(user_id, kind, year)
        serializer = LeaveBalanceSerializer(balances, many=True)
        return Response(serializer.data)


class ReportingLineView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.admin.manage")]

    def get(self, request, user_id, *args, **kwargs):
        line = admin.get_reporting_line(user_id)
        if line is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReportingLineSerializer(line)
        return Response(serializer.data)

    def put(self, request, user_id, *args, **kwargs):
        data = request.data
        admin.set_reporting_line(user_id, data["unit_head_id"], data.get("establishment_id"), data.get("sanctioning_authority_id"))
        line = admin.get_reporting_line(user_id)
        serializer = ReportingLineSerializer(line)
        return Response(serializer.data)
