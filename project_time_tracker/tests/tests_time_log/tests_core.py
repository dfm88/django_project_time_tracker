import datetime
from functools import partial

from django.forms import ValidationError
from django.utils import timezone

from tests import factories
from tests.base import BaseApiTest
from time_log.core import _check_ranges_dont_overlap, calculate_spent_time
from time_log.crud import time_log_crud


class TimeLogCoreTest(BaseApiTest):

    def test_time_logs_dont_overlap(self):
        """
        GIVEN two 'time_log' and 'other_time_log' instances

        WHEN 'time_log' and 'other_time_log' don't overlap
        THEN no exception is raised

        WHEN 'other_time_log' has no end_time ('other_time_log'
             wasn't closed before inserting a new 'time_log')
        THEN django.formsValidationError is raised

        WHEN 'time_log' and 'other_time_log' overlaps
        THEN django.formsValidationError is raised
        """
        utc_datetime = partial(datetime.datetime, tzinfo=timezone.utc)
        time_log = factories.TimeLogFactory.build()
        other_time_log = factories.TimeLogFactory.build()

        # don't overlaps
        time_log.start_time = utc_datetime(2022, 3, 1, 9, 00)
        time_log.end_time = utc_datetime(2022, 3, 1, 11, 00)
        other_time_log.start_time = utc_datetime(2022, 3, 1, 13, 00)
        other_time_log.end_time = utc_datetime(2022, 3, 1, 15, 00)
        self.assertEqual(
            _check_ranges_dont_overlap(
                time_log=time_log,
                other_time_log=other_time_log
            ),
            None
        )

        # other_time_log not closed
        time_log.start_time = utc_datetime(2022, 3, 1, 9, 00)
        time_log.end_time = utc_datetime(2022, 3, 1, 11, 00)
        other_time_log.start_time = utc_datetime(2022, 3, 1, 13, 00)
        other_time_log.end_time = None
        with self.assertRaises(ValidationError):
            _check_ranges_dont_overlap(
                time_log=time_log,
                other_time_log=other_time_log
            )

        # overlaps
        time_log.start_time = utc_datetime(2022, 3, 1, 9, 00)
        time_log.end_time = utc_datetime(2022, 3, 1, 11, 00)
        other_time_log.start_time = utc_datetime(2022, 3, 1, 10, 00)
        other_time_log.end_time = utc_datetime(2022, 3, 1, 12, 00)
        with self.assertRaises(ValidationError):
            _check_ranges_dont_overlap(
                time_log=time_log,
                other_time_log=other_time_log
            )

    def test_time_log_total_time(self):
        """
        GIVEN userA1 that is assigned to projA and logged twice (7h)
            userA2 that is assigned to projA and logged once (3h)
            userB1 that is assigned to projB and logged once (not closed)

        WHEN calculate_spent_time function is called for all projA
        THEN '10:00:00' is returned

        WHEN calculate_spent_time function is called for projA user A2
        THEN '3:00:00' is returned

        WHEN calculate_spent_time function is called for all projB
        THEN '0:00:00' is returned
        """
        # 10h
        time_logs_projA = time_log_crud.get_logs_for_statistics(
            project_id=self.projA.id,
            user=None
        )
        tot_time = calculate_spent_time(
            time_logs=time_logs_projA
        )
        self.assertEqual(tot_time, '10:00:00')

        # 3h
        time_logs_projA_userA2 = time_log_crud.get_logs_for_statistics(
            project_id=self.projA.id,
            user=self.userA2.id
        )
        tot_time = calculate_spent_time(
            time_logs=time_logs_projA_userA2
        )
        self.assertEqual(tot_time, '3:00:00')

        # 0h
        time_logs_projB = time_log_crud.get_logs_for_statistics(
            project_id=self.projB.id,
        )
        tot_time = calculate_spent_time(
            time_logs=time_logs_projB
        )
        self.assertEqual(tot_time, '0:00:00')
