from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from issuetrack.models import Project
from scripts.create_test_users import UserCreater
from scripts.data.test_users import issue_track_test_users as users
'''
    * reverse imported for use with calling views.
    * TestCase imported for LoginTest.
    * Client imported for instantiating web client.
    * User imported for creating and testing with a created user in the system.
    * Project imported as main model for this test.
    * UserCreater imported to create test users in setUp().
    * users imported to provide test user data.
'''


class ProjectTest(TestCase):
    ''' Test to add, read, delete and update Projects.
    '''

    def setUp(self):
        ''' Objects and routines that are set up for each test method.
        '''

        admin_user = User.objects.create(
            username='admin',
            email='admin@localhost',
            is_superuser=True,
            is_staff=True,
        )
        ''' admin_user is the top superuser this should work with.
        '''

        admin_user.set_password('admin')
        ''' Set the admin user's password to 'admin'.
        '''

        admin_user.save()
        ''' Save the admin's data.
        '''

        uc = UserCreater()
        ''' Instantiate a UserCreater class.
        '''
        uc.create_test_users(users)
        ''' UserCreater creates the test users.
        '''

    def test_create_users(self):
        ''' Test for create_test_users in setUp() to make sure the users
        are created.
        '''

        for username in [u['username'] for u in users]:
            user = User.objects.get(username=username)
            self.assertTrue(user)
            ''' Expecting all usernames in the list to be valid.
            '''

    def test_add_project_by_admin(self):
        ''' Test for adding projects by the admin user.
        '''

        c = Client()
        ''' Instantiate a test client.
        '''

        c.post(
            reverse('login'),
            {
                'username': 'admin',
                'password': 'admin',
            },
        )
        ''' Login the admin user.
        '''

        response = c.post(
            reverse('add_project'),
            {
                'name': 'Test Project1',
                'key': 'TP1',
                'owner': '1',
                'description': 'This is Test Project1',
                'members': ['1', '2', ],
            }
        )
        ''' Get the response from simulating adding a new project.
        '''

        self.assertEqual(response.status_code, 302)
        ''' Expecting a redirect if this is a successful project add.
        '''

        self.assertTrue(Project.objects.get(name='Test Project1'))
        ''' Expecting that the Test Project1 Project object was created.
        '''
