import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from tests.base import BaseApiTest


class TimeLogApiTest(BaseApiTest):
    @classmethod
    def setUpClass(cls):
        # apis
        cls.api_list_create = 'list_create__time_log'
        cls.api_retrieve_update_delete = 'retrieve_update_delete__time_log'

        super(TimeLogApiTest, cls).setUpClass()

    def test_permissions_on_get_list(self):
        """
        GIVEN userA1 that is assigned to projA and logged twice
              userA2 that is assigned to projA and logged once
              userB1 that is assigned to projB and logged once

        WHEN these users access to time_log list

        THEN userA1 and userA2 can see only time_logs of projA (3 logs)
             userB1 can see only time_logs of projB (1 logs)
             userB1 can't see logs of projA
        """
        url = reverse(self.api_list_create)
        url_qp = f'{url}?project_id={self.projA.id}'
        # userA1 - projA
        self.client.force_login(user=self.userA1)
        resp = self.client.get(url_qp)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_data), 3)
        # userA2 - projA
        self.client.force_login(user=self.userA2)
        resp = self.client.get(url_qp)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_data), 3)

        # userB1 - projB
        url_qp = f'{url}?project_id={self.projB.id}'
        self.client.force_login(user=self.userB1)
        resp = self.client.get(url_qp)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_data), 1)
        # userB1 - projA
        url_qp = f'{url}?project_id={self.projA.id}'
        resp = self.client.get(url_qp)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_id_queryparam_required(self):
        """
        GIVEN userA1 that is assigned to projA and logged twice

        WHEN these users access to time_log list and doesn't
             specify the ?project_id query param

        THEN userA1 receives a Bad Request
        """
        url = reverse(self.api_list_create)
        url_qp = f'{url}?project_id='
        # userA1 - projA
        self.client.force_login(user=self.userA1)
        resp = self.client.get(url_qp)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_permissions_on_create(self):
        """
        GIVEN userA2 hat is assigned to projA
              userB1 hat is assigned to projB

        WHEN userA2 creates a time_log in projA
        THEN userA2 creates the log

        WHEN userB1 creates a time_log in projA
        THEN userB1 can't create the log
        """
        url = reverse(self.api_list_create)
        url_qp = f'{url}?project_id={self.projA.id}'
        body = {
            'start_time': datetime.datetime(2023, 1, 1, tzinfo=timezone.utc)
        }
        # userA
        self.client.force_login(user=self.userA2)
        resp = self.client.post(url_qp, data=body)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # userB
        self.client.force_login(user=self.userB1)
        resp = self.client.post(url_qp, data=body)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_on_get_detail(self):
        """
        GIVEN userA1 that is assigned to projA
              userB1 that is assigned to projB

        WHEN userA1 read a log related to projA
        THEN userA1 can see it

        WHEN userA1 read a log related to projB
        THEN userA1 can't see it
        """
        url_time_logA = reverse(
            self.api_retrieve_update_delete,
            kwargs={'time_log_id': self.tl_userA1_projA_7h.id}
        )
        url_time_logB = reverse(
            self.api_retrieve_update_delete,
            kwargs={'time_log_id': self.tl_userB1_projB_partial.id}
        )

        # userA access to log of projA
        self.client.force_login(user=self.userA1)
        resp = self.client.get(url_time_logA)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # userA can't access log of projB
        resp = self.client.get(url_time_logB)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_on_edit(self):
        """
        GIVEN userA1 that is assigned to projA
              userA2 that is assigned to projA

        WHEN userA1 edit his log related to projA
        THEN userA1 can edit it

        WHEN userA1 edit a log related to projA of userA2
        THEN userA1 can't edit it
        """
        url_time_logA1 = reverse(
            self.api_retrieve_update_delete,
            kwargs={'time_log_id': self.tl_userA1_projA_7h.id}
        )
        url_time_logA2 = reverse(
            self.api_retrieve_update_delete,
            kwargs={'time_log_id': self.tl_userA2_projA_partial.id}
        )
        body = {
            'start_time': datetime.datetime(2023, 1, 1, tzinfo=timezone.utc)
        }
        # userA1 to his projA log
        self.client.force_login(user=self.userA1)
        resp = self.client.put(
            url_time_logA1,
            data=body,
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # userA1 to userA2 projA log
        resp = self.client.put(
            url_time_logA2,
            data=body,
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_on_delete(self):
        """
        GIVEN userA1 that is assigned to projA
              userA2 that is assigned to projA

        WHEN userA1 delete his log related to projA
        THEN userA1 can delete it

        WHEN userA1 delete a log related to projA of userA2
        THEN userA1 can't delete it
        """
        url_time_logA1 = reverse(
            self.api_retrieve_update_delete,
            kwargs={'time_log_id': self.tl_userA1_projA_7h.id}
        )
        url_time_logA2 = reverse(
            self.api_retrieve_update_delete,
            kwargs={'time_log_id': self.tl_userA2_projA_partial.id}
        )
        # userA1 to his projA log
        self.client.force_login(user=self.userA1)
        resp = self.client.delete(url_time_logA1)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # userA1 to userA2 projA log
        resp = self.client.delete(url_time_logA2)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
