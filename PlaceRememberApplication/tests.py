from django.test import TestCase
from PlaceRememberApplication.models import Remember
from django.contrib.auth.models import User

# Create your tests here.
class RememberModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create()
        Remember.objects.create(name='New_remember', description='Descr1', user=User.objects.get(id=1), latitude=10.1, longitude=12.2)

    def test_name_label(self):
        remember=Remember.objects.get(id=1)
        field_label = remember._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'Название воспоминания')

    def test_description_label(self):
        remember=Remember.objects.get(id=1)
        field_label = remember._meta.get_field('description').verbose_name
        self.assertEquals(field_label,'Описание')

    def test_latitude_max_length(self):
        remember=Remember.objects.get(id=1)
        max_length = remember._meta.get_field('latitude').max_length
        self.assertEquals(max_length,100)


class RememberListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('one','myemail@test.com', 'two')
        number_of_remembers = 10
        for remember_num in range(number_of_remembers):
            Remember.objects.create(name='Remember %s' % remember_num, description='description %s' % remember_num, user=User.objects.get(id=1), latitude=10.1, longitude=12.2 )

    def test_view_url_without_login(self):
        resp = self.client.get('/remembers/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='one', password='two')
        resp = self.client.get('/remembers/')
        self.assertEqual(resp.status_code, 200)

    def test_pagination_is_six(self):
        self.client.login(username='one', password='two')
        resp = self.client.get('/remembers/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 6)

    def test_lists_all_remembers(self):
        self.client.login(username='one', password='two')
        resp = self.client.get('/remembers/' + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 4)