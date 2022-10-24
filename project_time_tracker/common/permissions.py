from rest_framework import permissions

from projects.models import Project
from time_log.models import TimeLog


class IsAssignedToProjectOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow assigned to a project
    """
    message = 'User is not assigned to this project'

    def has_object_permission(self, request, view, obj: Project):
        if request.user in obj.assignees.all():
            return True
        return request.user.is_staff


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


class IsAdminForWriting(permissions.IsAdminUser):
    """
    Extends rest_framework IsAdminUser permission limiting it to
    write API methods
    """
    message = 'Not enough permissions to write'

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return super().has_permission(request, view)
