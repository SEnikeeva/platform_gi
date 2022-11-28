from django.db import models
from django.contrib.auth import get_user_model

from rest.models import Project, Coords
from users.models import Company


class CoordsDiff(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL
    )
    company = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project,
        related_name='coords_diffs',
        on_delete=models.CASCADE,
    )
    origin = models.ForeignKey(
        Coords,
        related_name='origins',
        on_delete=models.CASCADE,
    )

    changed = models.ForeignKey(
        Coords,
        related_name='changes',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['project']
