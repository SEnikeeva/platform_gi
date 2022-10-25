from django.contrib import admin

# Register your models here.
from rest.models import *


admin.site.register(Project)
admin.site.register(OilDeposit)
admin.site.register(Well)
admin.site.register(Coords)
admin.site.register(Perforation)
