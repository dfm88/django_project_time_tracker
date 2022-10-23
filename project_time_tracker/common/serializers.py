from .models import BaseModel


class BaseMeta:
    model = BaseModel
    exclude = ('created_at', 'updated_at',)
