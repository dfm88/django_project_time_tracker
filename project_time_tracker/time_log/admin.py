from django.contrib import admin

from time_log.models import TimeLog


class TimeLogAdmin(admin.ModelAdmin):
    list_filter = (
        'project_assignment__project',
        'project_assignment__user',
    )


admin.site.register(TimeLog, TimeLogAdmin)
