from django.contrib import admin
from .models import Bug


class BugAdmin(admin.ModelAdmin):
    readonly_fields = ('report_date',)


admin.site.register(Bug, BugAdmin)


