from common.permissions import IsAssignedToProjectOrAdmin
from projects.crud import project_crud
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView


class ProjectIdPermissionMixin(APIView):
    permission_classes = (IsAssignedToProjectOrAdmin,)

    """Override `initial` method of ApiVIEW"""
    def initial(self, request, *args, **kwargs):
        """
        Returns the initial request object with additional
        kwargs['project']: Project if`project_id` is passes as query param

        Checks if request.user is assigned to project

        Args:
            request:

        Raises:
            ParseError: if query_param `project_id` was not passed
        """
        super().initial(request, *args, **kwargs)
        project_id = self.request.query_params.get('project_id')
        if not project_id:
            raise ParseError('project_id query param is required')

        proj = project_crud.get_by(pk=project_id)
        self.check_object_permissions(request, proj)

        # add project_id to context
        request.parser_context['kwargs']['project'] = proj
