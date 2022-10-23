from django.contrib import admin

from .models import TimeLog


class TimeLogAdmin(admin.ModelAdmin):
    list_filter = (
        'project_assignee__project',
        'project_assignee__user',
    )


admin.site.register(TimeLog, TimeLogAdmin)
