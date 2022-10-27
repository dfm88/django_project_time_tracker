import datetime

from django.test import TestCase, override_settings
from django.utils import timezone

from tests import factories


@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
})
class BaseApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        setting up the following scenario
        ---------------------------------------------------
        |PROJ | USERS  |             TIME LOGS             |
        ---------------------------------------------------
            user_admin

        projA
            ├── userA1
            |     ├─────── 2022-02-01 11:00:00 - 2022-02-01 18:00 (7h)
            |     └─────── 2022-03-01 11:00:00 - None
            |
            └── userA2
                  └─────── 2022-02-01 11:00:00 - 2022-03-01 14:00 (3h)

        projB
            └── userB1
                  └─────── 2022-03-01 15:00:00 - None
        --------------
        """
        # create users
        cls.user_admin = factories.AdminFactory()
        cls.userA1 = factories.UserFactory(username='userA1')
        cls.userA2 = factories.UserFactory(username='userA2')
        cls.userB1 = factories.UserFactory(username='userB1')
        super(BaseApiTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseApiTest, cls).tearDownClass()

    def setUp(self):
        # assign users and create projects

        # projects
        self.projA = factories.ProjectFactory(name='projA', creator=self.user_admin)
        self.projB = factories.ProjectFactory(name='projB', creator=self.user_admin)

        # userA1 to projA
        self.userA1_projA = factories.ProjectAssignmentFactory(
            user=self.userA1,
            project=self.projA,
        )
        # userA2 to projA
        self.userA2_projA = factories.ProjectAssignmentFactory(
            user=self.userA2,
            project=self.projA,
        )
        # userB1 to projB
        self.userB1_projB = factories.ProjectAssignmentFactory(
            user=self.userB1,
            project=self.projB
        )

        # logs of userA1 to projA
        self.tl_userA1_projA_7h = factories.TimeLogCompleteFactory7h(
            project_assignment=self.userA1_projA
        )
        self.tl_userA1_projA_3h = factories.TimeLogOnlyStartFactory(
            project_assignment=self.userA1_projA
        )
        # logs of userA2 to projA
        self.tl_userA2_projA_partial = factories.TimeLogCompleteFactory3h(
            project_assignment=self.userA2_projA
        )
        # logs of userB1 to projB
        self.tl_userB1_projB_partial = factories.TimeLogOnlyStartFactory(
            project_assignment=self.userB1_projB,
            start_time=datetime.datetime(
                year=2022,
                month=3,
                day=1,
                hour=15,
                minute=00,
                tzinfo=timezone.utc
            )
        )

        super(BaseApiTest, self).setUp()

    def tearDown(self):
        super(BaseApiTest, self).tearDown()
