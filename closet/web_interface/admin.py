from django.contrib import admin
from .models import Personnel, Expenses, Log, Notes


# @admin.register(Personnel)
# class ModelAAdmin(admin.ModelAdmin):
#     search_fields = ['lastName', 'firstName']

# Register your models here.


admin.site.register(Personnel)
admin.site.register(Expenses)
admin.site.register(Log)
admin.site.register(Notes)
