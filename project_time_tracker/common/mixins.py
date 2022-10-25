from dataclasses import dataclass

from rest_framework.exceptions import ParseError
from rest_framework.views import APIView

from common.crud import BaseCRUD


@dataclass
class ObjectFromIdMixin(APIView):
    crud_instance: BaseCRUD
    lookup_name: str
    injection_name: str
    required: bool = False
    required_error_msg: str = "Can't find lookup value in request"

    """Override `initial` method of ApiVIEW"""
    def initial(self, request, *args, **kwargs):
        """
        Returns the initial request object injecting a models.Model instance in
        request's kwargs[self.injection_name] calling the default self.crud_instance
        `get_by` method with the `pk` as key and lookup_name as value.


        Args:
            request:

        Raises:
            rest_framework.exceptions.NotFound: if object doesn't exists
            rest_framework.exceptions.NotAcceptable: if multiple objects are returned
            rest_framework.exceptions.ParseError: if required is True and lookup_name not in kwargs

        """
        super().initial(request, *args, **kwargs)

        lookup_value = kwargs.get(self.lookup_name)

        item = None
        if not lookup_value:
            if self.required:
                raise ParseError(self.required_error_msg)

        else:
            item = self.crud_instance.get_by(pk=lookup_value)

        # add project_id to context
        request.parser_context['kwargs'][self.injection_name] = item
