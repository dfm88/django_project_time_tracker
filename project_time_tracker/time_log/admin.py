from django.contrib import admin

from .models import TimeLog


class TimeLogAdmin(admin.ModelAdmin):
    list_filter = ('project',)


admin.site.register(TimeLog, TimeLogAdmin)
