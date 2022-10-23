
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from time_log.models import TimeLog

from django.forms import ValidationError


def ensure_log_assigned_project(time_log: "TimeLog") -> None:
    """Checks that logger user is logging to an assigned project

    Args:
        time_log (TimeLog)

    Raises:
        ValidationError
    """
    if time_log.project not in time_log.user.assigned_projects.all():
        raise ValidationError(
            f"Project {time_log.project} does not belong to user {time_log.user}"
        )
