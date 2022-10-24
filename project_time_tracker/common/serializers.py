from rest_framework import serializers

from .models import BaseModel


class BaseMeta:
    model = BaseModel
    exclude = ('created_at', 'updated_at',)


def serialize_input_data(
    serializer: serializers.Serializer,
    data: dict
) -> dict:
    """Validate input data and returns validated one

    Args:
        data (dict): data with which build the Model object

    Raises:
        ValidationError: if serializer is not valid

    Returns:
        dict: validated data dict
    """
    serializer_instance = serializer(data=data)
    if serializer_instance.is_valid(raise_exception=True):
        return serializer_instance.data
