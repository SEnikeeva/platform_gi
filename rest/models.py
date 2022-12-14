from django.db import models
from django.contrib.auth import get_user_model

from users.models import Company


class Project(models.Model):
    name = models.CharField(max_length=50)

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
        on_delete=models.SET_NULL,
        null=True
    )
    company = models.ForeignKey(
        Company,
        null=True,
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
    project = models.ForeignKey(
        Project,
        related_name='wells',
        on_delete=models.SET_NULL,
        null=True
    )
    company = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.CASCADE
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
    company = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.CASCADE
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
    project = models.ForeignKey(
        Project,
        related_name='coords',
        on_delete=models.SET_NULL,
        null=True
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
    company = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project,
        related_name='perforations',
        on_delete=models.SET_NULL,
        null=True
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
        return f"{self.well}, {self.layer}"

    class Meta:
        ordering = ['date']


class EORProd(models.Model):
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
        related_name='eor_prods',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='eor_prods',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='eor_prods',
        on_delete=models.CASCADE,
    )
    level = models.CharField(max_length=50, null=True)
    layer = models.CharField(max_length=50, null=True)
    date = models.DateTimeField()
    work_hours = models.FloatField()
    q_oil = models.FloatField()
    q_water = models.FloatField()
    fluid_rate = models.FloatField()
    sgw = models.FloatField(null=True)

    def __str__(self):
        return f"{self.well}, {self.date}"

    class Meta:
        ordering = ['date']


class EORInj(models.Model):
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
        related_name='eor_injs',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='eor_injs',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='eor_injs',
        on_delete=models.CASCADE,
    )
    level = models.CharField(max_length=50, null=True)
    layer = models.CharField(max_length=50, null=True)
    date = models.DateTimeField()
    work_hours = models.FloatField()
    q_water3 = models.FloatField()
    acceleration = models.FloatField()
    agent_code = models.FloatField()

    def __str__(self):
        return f"{self.well}, {self.date}"

    class Meta:
        ordering = ['date']


class Mineralization(models.Model):
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
        related_name='mineralizations',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='mineralizations',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='mineralizations',
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    type = models.IntegerField()

    def __str__(self):
        return f"{self.well}, {self.type}"

    class Meta:
        ordering = ['start_date']


class WCReason(models.Model):
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
        related_name='wc_reasons',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='wc_reasons',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='wc_reasons',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    category = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.well}, {self.type}"

    class Meta:
        ordering = ['date']


class Pressure(models.Model):
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
        related_name='pressures',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='pressures',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='pressures',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    pressure = models.FloatField()
    type = models.CharField(max_length=255, null=True)
    q_fluid = models.FloatField(null=True)
    level = models.CharField(max_length=50, null=True)
    productivity = models.FloatField(null=True)
    mark = models.FloatField(null=True)

    def __str__(self):
        return f"{self.well}, {self.pressure}"

    class Meta:
        ordering = ['date']


class Work(models.Model):
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
        related_name='works',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='works',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='works',
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.well}, {self.type}"

    class Meta:
        ordering = ['start_date']


class PressureRecoveryCurve(models.Model):
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
        related_name='prcs',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='prcs',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='prcs',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    productivity = models.FloatField()
    level = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.well}, {self.productivity}"

    class Meta:
        ordering = ['date']


class WaterAnalysis(models.Model):
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
        related_name='water_analysis',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='water_analysis',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='water_analysis',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    level = models.CharField(max_length=50)
    mineralization = models.FloatField()
    sulfate = models.FloatField()

    def __str__(self):
        return f"{self.well}, {self.mineralization}"

    class Meta:
        ordering = ['date']
