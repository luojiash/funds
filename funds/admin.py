from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Me)
admin.site.register(models.Record)
admin.site.register(models.Assumption)
admin.site.register(models.Income)
admin.site.register(models.Other)
admin.site.register(models.Deposit)
admin.site.register(models.Loan)


