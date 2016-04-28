from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
''' reverse imported for use with calling views.
    TestCase imported for LoginTest.
    Client imported for instantiating web client.
    User imported for creating and testing with a created user in the system.
'''


class LoginTest(TestCase):
    ''' Class to test logins with users.
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

    def test_admin_user_created(self):
        ''' A test to make sure that the admin user was created as expected.
        '''

        user = User.objects.get(username='admin')
        ''' Get the admin user model object.
        '''

        self.assertTrue(user.username == 'admin')
        ''' Test to make sure this is the user expected.
        '''

    def test_access_index_without_creds(self):
        ''' A test to see what kind of status code we get if we try to access
        the main page without logging in first. We should get a redirect
        code: 302.
        '''

        c = Client()
        ''' Create the client object.
        '''

        response = c.get(
            reverse('index'),
        )
        ''' Get the response from accessing /issuetrack/.
        '''

        self.assertEquals(response.status_code, 302)
        ''' We should get redirected back to the login page.
        '''

    def test_access_index_with_creds(self):
        ''' A test to see what kind of status code we get if we try to
        access the main page while logging in first. We should get a
        success code: 200.
        '''

        c = Client()
        ''' Create the client object.
        '''

        response = c.post(
            reverse('login'),
            {
                'username': 'admin',
                'password': 'admin',
            },
            next=reverse('index'),
        )
        ''' Do a POST request to the login page with username and password.
        The redirect ("next") should be to 'index' view.
        '''

        self.assertEquals(response.status_code, 302)
        ''' We are expecting a 302 (redirect) status code.
        '''

        response = c.get(
            reverse('index'),
        )
        ''' Now, we try to access the 'index' view.
        '''

        self.assertEquals(response.status_code, 200)
        ''' We are expecting this time a 200 (success) status code.
        '''

        expected = (
            'Issues List', 'All', 'Open', 'Closed', 'Title', 'Kind',
            'Priority', 'Status', 'Asignee', 'Created', 'Modified',
            'Home', 'Projects', 'Create New Issue', 'Add New Project',
        )
        ''' A list of strings we are expecting to see when we access the
        'index' view.
        '''

        for each in expected:
            self.assertTrue(each in str(response.content))
        ''' We are expecting all strings to be in the view's content.
        '''
