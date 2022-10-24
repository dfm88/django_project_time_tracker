from rest_framework import permissions

from common.permissions import IsAssignedToProjectOrAdmin

from .models import TimeLog


class IsLogOwnerOrAdmin(IsAssignedToProjectOrAdmin):
    """
    Object-level permission to only Users that are
    part of the project (READ), or are owner of the log (WRITE)
    """
    message = 'Can`t write on others logs'

    def has_object_permission(self, request, view, time_log: TimeLog):

        # check in parent method if user is in project
        user_in_project = super().has_object_permission(
            request=request,
            view=view,
            obj=time_log.project_assignment.project
        )
        if not user_in_project:
            self.message = super().message
            return False

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Request User must be the logger to write the object
        if time_log.project_assignment.user == request.user:
            return True

        return request.user.is_staff
