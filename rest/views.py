from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from .serializers import *


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.prefetch_related(
            Prefetch(
                'oil_deposits',
                queryset=OilDeposit.objects.all()
            )
        ).filter(author=self.request.user)


class OilDepositViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OilDepositSerializer

    def get_queryset(self):
        return OilDeposit.objects.prefetch_related(
            Prefetch(
                'wells',
                queryset=Well.objects.all()
            )
        ).filter(author=self.request.user)


class WellViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WellSerializer

    def get_queryset(self):
        return Well.objects.filter(author=self.request.user)
