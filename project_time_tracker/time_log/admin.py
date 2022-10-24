from django.contrib import admin

from .models import TimeLog


class TimeLogAdmin(admin.ModelAdmin):
    list_filter = (
        'project_assignment__project',
        'project_assignment__user',
    )


admin.site.register(TimeLog, TimeLogAdmin)
