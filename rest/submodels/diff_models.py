from django.db import models

from rest.models import Project, Coords, Perforation
from rest.submodels.abstract_models import AuthorCompanyModel


class CoordsDiff(AuthorCompanyModel):
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


class PerforationDiff(AuthorCompanyModel):
    project = models.ForeignKey(
        Project,
        related_name='perforation_diffs',
        on_delete=models.CASCADE,
    )
    origin = models.ForeignKey(
        Perforation,
        related_name='origins',
        on_delete=models.CASCADE,
    )

    changed = models.ForeignKey(
        Perforation,
        related_name='changes',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['project']
