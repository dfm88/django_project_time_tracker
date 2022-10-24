from dataclasses import dataclass, field

from common.mixins import ObjectFromIdMixin
from time_log.crud import TimeLogCRUD, time_log_crud


@dataclass
class TimeLogFromIdMixin(ObjectFromIdMixin):
    crud_instance: TimeLogCRUD = field(default=time_log_crud)
    lookup_name: str = 'time_log_id'
    injection_name: str = 'time_log'
