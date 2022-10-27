from django.urls import reverse
from rest_framework import status

from tests.base import BaseApiTest


class ProjectApiTest(BaseApiTest):
    @classmethod
    def setUpClass(cls):

        # apis
        cls.api_list_create = 'list_create__project'
        cls.api_retrieve_update_delete = 'retrieve_update_delete__project'
        cls.api_handle_users = 'handle_users__project'
        cls.api_statistics = 'statistics__project'
        super(ProjectApiTest, cls).setUpClass()

    def test_time_log_dont_overlap(self):
        """
        GIVEN userA1 that is assigned to projA
              userB1 that is assigned to projB
              user_admin that is admin

        WHEN these users access to project list

        THEN userA1 can see only projA
             userB1 can see only projB
             admin sees both projects
        """
        url = reverse(self.api_list_create)
        # userA
        self.client.force_login(user=self.userA1)
        resp = self.client.get(url)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual(resp_data[0]['id'], self.projA.id)

        # userB
        self.client.force_login(user=self.userB1)
        resp = self.client.get(url)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual(resp_data[0]['id'], self.projB.id)

        # admin
        self.client.force_login(user=self.user_admin)
        resp = self.client.get(url)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_data), 2)

    def test_permissions_on_create(self):
        """
        GIVEN userA1 that is not admin
              user_admin that is admin

        WHEN userA1 creates a project
        THEN userA1 is forbidden

        WHEN admin creates a project
        THEN project is created and creator is admin
        """
        url = reverse(self.api_list_create)
        new_proj_name = 'projC'
        new_proj_descr = 'projC descr'
        body = {
            'name': new_proj_name,
            'description': new_proj_descr
        }
        # userA
        self.client.force_login(user=self.userA1)
        resp = self.client.post(url, data=body)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # admin
        self.client.force_login(user=self.user_admin)
        resp = self.client.post(url, data=body)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_data['name'], new_proj_name)

    def test_permissions_on_get_detail(self):
        """
        GIVEN userA1 that is assigned to projA
              userB1 that is assigned to projB
              user_admin that is admin

        WHEN userA1 read projA
        THEN userA1 can see it

        WHEN userA1 read projB
        THEN userA1 can't see it
        """
        url_projA = reverse(
            self.api_retrieve_update_delete,
            kwargs={'project_id': self.projA.id}
        )
        url_projB = reverse(
            self.api_retrieve_update_delete,
            kwargs={'project_id': self.projB.id}
        )

        # userA access to projA
        self.client.force_login(user=self.userA1)
        resp = self.client.get(url_projA)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_data['id'], self.projA.id)

        # userA can't access to projB
        resp = self.client.get(url_projB)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_on_edit(self):
        """
        GIVEN userA1 that is not admin and is assigned to projA
              user_admin that is admin

        WHEN userA1 edits a projectA
        THEN userA1 is forbidden

        WHEN admin edit projectA
        THEN project is edited
        """
        url_projA = reverse(
            self.api_retrieve_update_delete,
            kwargs={'project_id': self.projA.id}
        )
        new_proj_name = 'new_proj'
        new_proj_descr = self.projA.description
        body = {
            'name': new_proj_name,
            'description': new_proj_descr
        }
        # userA
        self.client.force_login(user=self.userA1)
        resp = self.client.put(url_projA, data=body, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # admin
        self.client.force_login(user=self.user_admin)
        resp = self.client.put(url_projA, data=body, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_permissions_on_delete(self):
        """
        GIVEN userA1 that is not admin and is assigned to projA
              user_admin that is admin

        WHEN userA1 deletes a projectA
        THEN userA1 is forbidden

        WHEN admin delete projectA
        THEN project is deleted
        """
        url_projA = reverse(
            self.api_retrieve_update_delete,
            kwargs={'project_id': self.projA.id}
        )
        # userA
        self.client.force_login(user=self.userA1)
        resp = self.client.delete(url_projA)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # admin
        self.client.force_login(user=self.user_admin)
        resp = self.client.delete(url_projA)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
