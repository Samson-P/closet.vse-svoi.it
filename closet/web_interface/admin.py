from django.contrib import admin
from .models import *


# @admin.register(Personnel)
# class ModelAAdmin(admin.ModelAdmin):
#     search_fields = ['lastName', 'firstName']

# Register your models here.


admin.site.register(Personnel)
admin.site.register(Expenses)
admin.site.register(Log)
admin.site.register(Notes)
admin.site.register(TechnicalSupport)
