from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    name = models.CharField(max_length=50)

    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class OilDeposit(models.Model):
    name = models.CharField(max_length=50)

    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL
    )
    project = models.ForeignKey(
        Project,
        related_name='oil_deposits',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Well(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='wells',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
