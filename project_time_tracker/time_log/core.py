
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from time_log.models import TimeLog

from django.forms import ValidationError

from .crud import time_log_crud


def _check_ranges_dont_overlap(
    time_log: "TimeLog",
    other_time_log: "TimeLog",
) -> None:
    """Given a TimeLog object, ensures that it was closed
    (e.g. other_time_log.end_time == None)

    And that ranges don't overlap

    Args:
        time_log (TimeLog) TimeLog to verify
        other_time_log (TimeLog) TimeLog to compare with

    Raises:
        ValidationError

    Returns:
        None
    """
    # check whether other time_log wasn't closed
    if other_time_log.end_time is None:
        raise ValidationError(
            f'You should close this time log first: "{other_time_log}"'
        )

    # checks that time range don't overlap
    max_start_time = max(
        time_log.start_time, other_time_log.start_time
    )
    min_end_time = min(
        time_log.end_time, other_time_log.end_time
    )

    if (min_end_time - max_start_time).total_seconds() > 0:
        raise ValidationError(
            f'This time log: "{time_log}" overlaps with: "{other_time_log}"'
        )


def ensure_ranges_dont_overlap(time_log: "TimeLog") -> None:
    """Given a TimeLog object, ensures that for the same Project
    and for the same user, there aren't overlapping times

    Args:
        time_log (TimeLog)

    Raises:
        ValidationError
    """
    project_id: int = time_log.project_assignment.project.id
    user_id: int = time_log.project_assignment.user.id

    # takes all other logs of same user in same project,
    # excluding the log passed as argument (in case of update)
    proj_time_log_per_user: TimeLog = time_log_crud.get_logs_by_user_project(
        project_id=project_id,
        user_id=user_id,
    ).exclude(pk=time_log.pk)

    for other_time_log in proj_time_log_per_user:
        _check_ranges_dont_overlap(
            time_log=time_log,
            other_time_log=other_time_log
        )
