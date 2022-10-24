from dataclasses import dataclass

from projects.mixins import ProjectFromIdMixin
from users.crud import user_crud


@dataclass
class UserIdQueryStringMixin(ProjectFromIdMixin):

    def initial(self, request, *args, **kwargs):
        """
        checks if `user_id` query param was passed
        and injects it in request kwargs
        """
        super().initial(request, *args, **kwargs)
        user = None
        user_id = self.request.query_params.get('user_id')
        if user_id:
            user = user_crud.get_by_or_none(pk=user_id)

        request.parser_context['kwargs']['user'] = user
