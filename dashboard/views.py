from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext as _
from users.models import User


class DashboardStatsView(APIView):
    def get(self, request):
        total_users = User.objects.customers().count()
        return Response({"total_customers": total_users}, status=200)
