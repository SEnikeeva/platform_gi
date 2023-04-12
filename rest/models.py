from django.db import models
from django.contrib.postgres.fields import HStoreField

from rest.submodels.abstract_models import AuthorCompanyModel
from users.models import Company


class Project(AuthorCompanyModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class OilDeposit(AuthorCompanyModel):
    name = models.CharField(max_length=50)

    project = models.ForeignKey(
        Project,
        related_name='oil_deposits',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Well(AuthorCompanyModel):
    name = models.CharField(max_length=50)
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Coords(AuthorCompanyModel):
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


class Perforation(AuthorCompanyModel):
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


class EORProd(AuthorCompanyModel):
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


class EORInj(AuthorCompanyModel):
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


class Mineralization(AuthorCompanyModel):
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


class WCReason(AuthorCompanyModel):
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


class Pressure(AuthorCompanyModel):
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


class Work(AuthorCompanyModel):
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


class PressureRecoveryCurve(AuthorCompanyModel):
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


class WaterAnalysis(AuthorCompanyModel):
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


class Isotopy(AuthorCompanyModel):
    project = models.ForeignKey(
        Project,
        related_name='isotopy',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='isotopy',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='isotopy',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    area = models.CharField(max_length=50, null=True)
    ngdu = models.CharField(max_length=50, null=True)
    level = models.CharField(max_length=50, null=True)
    layer = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=255, null=True)
    delta_D = models.FloatField()
    delta_18O = models.FloatField()

    def __str__(self):
        return f"{self.well}, {self.delta_D}, {self.delta_18O}"

    class Meta:
        ordering = ['date']


class WaterMicroMacro(AuthorCompanyModel):
    project = models.ForeignKey(
        Project,
        related_name='water_micro_macro',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='water_micro_macro',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='water_micro_macro',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    ngdu = models.CharField(max_length=50, null=True)
    area = models.CharField(max_length=50, null=True)
    device = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=255, null=True)
    layer = models.CharField(max_length=255, null=True)
    components = HStoreField(null=True)

    def __str__(self):
        return f"{self.well}, {self.date}"

    class Meta:
        ordering = ['date']


class OilMicroMacro(AuthorCompanyModel):
    project = models.ForeignKey(
        Project,
        related_name='oil_micro_macro',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='oil_micro_macro',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='oil_micro_macro',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    ngdu = models.CharField(max_length=50, null=True)
    area = models.CharField(max_length=50, null=True)
    device = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=255, null=True)
    components = HStoreField(null=True)

    def __str__(self):
        return f"{self.well}, {self.date}"

    class Meta:
        ordering = ['date']


class SixComponents(AuthorCompanyModel):
    project = models.ForeignKey(
        Project,
        related_name='six_components',
        on_delete=models.SET_NULL,
        null=True
    )
    well = models.ForeignKey(
        Well,
        related_name='six_components',
        on_delete=models.CASCADE,
    )
    oil_deposit = models.ForeignKey(
        OilDeposit,
        related_name='six_components',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    ngdu = models.CharField(max_length=50, null=True)
    unit = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=255, null=True)
    mineralization = models.FloatField()
    rigidity = models.FloatField()

    anions = HStoreField(null=True)
    cations = HStoreField(null=True)

    def __str__(self):
        return f"{self.well}, {self.date}"

    class Meta:
        ordering = ['date']

