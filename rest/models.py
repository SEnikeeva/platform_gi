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


class Coords(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL
    )
    well = models.ForeignKey(
        Well,
        related_name='coords',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='coords',
        on_delete=models.CASCADE,
    )
    x = models.FloatField()
    y = models.FloatField()
    level = models.CharField(max_length=50, null=True)
    layer = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.x}, {self.y}"

    class Meta:
        ordering = ['level']


class Perforation(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL
    )
    well = models.ForeignKey(
        Well,
        related_name='perforations',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='perforations',
        on_delete=models.CASCADE,
    )
    perf_type = models.CharField(max_length=255)
    date = models.DateTimeField()
    top = models.FloatField()
    bot = models.FloatField()
    layer = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.layer}, {self.top}"

    class Meta:
        ordering = ['layer']
