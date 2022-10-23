from rest_framework import permissions

from projects.models import Project


class IsAssignedToProjectOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow assigned to a project
    """
    message = 'User is not assigned to this project'

    def has_object_permission(self, request, view, obj: Project):
        if request.user in obj.assignees.all():
            return True
        return request.user.is_staff
