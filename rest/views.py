from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import *


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user).all()

