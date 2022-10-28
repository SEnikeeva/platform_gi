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
        return f"{self.well}, {self.layer}"

    class Meta:
        ordering = ['date']


class EORProd(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL
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
    work_hours = models.IntegerField()
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
    work_hours = models.IntegerField()
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

