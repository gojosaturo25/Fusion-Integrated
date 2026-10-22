from django.utils import timezone
from rest_framework import status
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
    def get_permissions(self):
        if self.request.method == "GET":
            return [HasModuleGrant("leave")(), HasPermission("leave.application.view_own")()]
        elif self.request.method == "POST":
            return [HasModuleGrant("leave")(), HasPermission("leave.application.apply")()]
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
        app = applications.apply_leave(user_id, request.principal.kind, data)
        return Response(LeaveApplicationSerializer(app).data, status=status.HTTP_201_CREATED)


class ApplicationDetailView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.view_own")]

    def get(self, request, pk, *args, **kwargs):
        app = selectors.visible_application(request.principal.user_id, pk)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class WithdrawView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.apply")]

    def post(self, request, pk, *args, **kwargs):
        applications.withdraw(request.principal.user_id, pk)
        app = selectors.visible_application(request.principal.user_id, pk)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class CancelView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.apply")]

    def post(self, request, pk, *args, **kwargs):
        today = timezone.localdate()
        app = lifecycle.request_cancellation(request.principal.user_id, pk, today)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class SubstituteResponseView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.substitute.respond")]

    def post(self, request, pk, *args, **kwargs):
        serializer = SubstituteResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        accept = data["accept"]
        app = applications.respond_to_substitute(request.principal.user_id, pk, accept)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class ReplaceSubstituteView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.apply")]

    def post(self, request, pk, *args, **kwargs):
        serializer = ReplaceSubstituteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        substitute_id = data["substitute_id"]
        app = applications.replace_substitute(request.principal.user_id, pk, substitute_id)
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
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.review")]

    def post(self, request, pk, *args, **kwargs):
        serializer = DecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        decision = data["decision"]
        remark = data.get("remark", "")

        app = selectors.visible_application(request.principal.user_id, pk)

        if app.stage == "establishment":
            if not request.principal.has_permission("leave.application.verify"):
                raise NotFoundError("You do not have permission to decide at this stage.")
        elif app.stage == "sanction":
            if not request.principal.has_permission("leave.application.sanction"):
                raise NotFoundError("You do not have permission to decide at this stage.")

        app = lifecycle.decide(request.principal.user_id, pk, decision, remark)
        serializer = LeaveApplicationSerializer(app)
        return Response(serializer.data)


class BalanceView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.application.view_own")]

    def get(self, request, *args, **kwargs):
        user_id = request.principal.user_id
        year = int(request.query_params.get("year", timezone.localdate().year))
        kind = request.principal.kind
        balances = admin.ensure_balances(user_id, kind, year)
        serializer = LeaveBalanceSerializer(balances, many=True)
        return Response(serializer.data)


class ReportingLineView(APIView):
    permission_classes = [HasModuleGrant("leave"), HasPermission("leave.admin.manage")]

    def get(self, request, user_id, *args, **kwargs):
        line = selectors.get_reporting_line(user_id)
        if line is None:
            raise NotFoundError()
        serializer = ReportingLineSerializer(line)
        return Response(serializer.data)

    def put(self, request, user_id, *args, **kwargs):
        serializer = ReportingLineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        line = admin.set_reporting_line(user_id, data["unit_head_id"], data.get("establishment_id"), data.get("sanctioning_authority_id"))
        serializer = ReportingLineSerializer(line)
        return Response(serializer.data)
