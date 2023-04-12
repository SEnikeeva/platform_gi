from django.contrib import admin

# Register your models here.
from rest.models import *
from rest.submodels.diff_models import *


admin.site.register(Project)
admin.site.register(OilDeposit)
admin.site.register(Well)
admin.site.register(Coords)
admin.site.register(Perforation)
admin.site.register(EORProd)
admin.site.register(EORInj)
admin.site.register(Mineralization)
admin.site.register(WCReason)
admin.site.register(Pressure)
admin.site.register(Work)
admin.site.register(PressureRecoveryCurve)
admin.site.register(WaterAnalysis)
admin.site.register(Isotopy)
admin.site.register(WaterMicroMacro)
admin.site.register(OilMicroMacro)
admin.site.register(SixComponents)

admin.site.register(CoordsDiff)
