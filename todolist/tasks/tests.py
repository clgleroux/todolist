# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Task

from django.urls import reverse
from django.test import TestCase

from django.contrib.auth.models import User


# Create your tests here.


class TestTask(TestCase):

    def setUp(self):
        self.username = 'john'
        self.password = 'djangodemo'
        self.user = User.objects.create_user(
            username=self.username,
            email="john@gmail.com",
            password=self.password)

    # OK
    def test_form_login_exists(self):
        create = reverse('login-home')
        response = self.client.get(create)
        self.assertEquals(response.status_code, 200)

    # OK
    def create_a_account_redirect(self):
        self.client.login(
            username=self.username,
            password=self.password)

        register = reverse("register")
        response = self.client.post(
            register,
            {
                "username": "First",
                "email": "demo@gmail.com",
                "password1": "djangodemo",
                "password2": "djangodemo"
            })
        self.assertEquals(User.objects.count(), 2)
        self.assertEquals(response.status_code, 302)

    # OK
    def create_a_account_not_valid(self):
        self.client.login(
            username=self.username,
            password=self.password)

        register = reverse("register")
        self.client.post(
            register,
            {
                "username": "First",
                "email": "demo@gmail.com",
                "password1": "djangodemo"
            })
        self.assertEquals(User.objects.count(), 1)

    # OK
    def test_list_view(self):
        self.client.login(
            username=self.username,
            password=self.password)

        descr1 = 'First description'
        descr2 = 'Second description'
        obj1 = Task(description=descr1)
        obj1.creator = self.user
        obj1.save()
        obj2 = Task(description=descr2)
        obj2.creator = self.user
        obj2.save()
        url = reverse('tasks:home')
        response = self.client.get(url)
        self.assertIn(descr1.encode(), response.content)
        self.assertIn(descr2.encode(), response.content)

    # OK
    def test_form_valid(self):
        self.client.login(
            username=self.username,
            password=self.password)

        create = reverse("tasks:home")
        response = self.client.post(
            create, {"description": "First todo"})
        self.assertEquals(Task.objects.count(), 1)
        self.assertEquals(response.status_code, 302)

    # OK
    def test_form_invalid(self):
        self.client.login(
            username=self.username,
            password=self.password)

        create = reverse("tasks:home")
        response = self.client.post(create, {})
        self.assertEquals(Task.objects.count(), 0)
        self.assertEquals(response.status_code, 400)

    # OK
    def test_form_valid_not_connect(self):
        create = reverse("tasks:home")
        self.client.post(
            create, {"description": "First todo"})
        self.assertEquals(Task.objects.count(), 0)

    # OK
    def test_from_delete(self):
        self.client.login(
            username=self.username,
            password=self.password)

        reverse("tasks:home")
        descr = 'First description'
        obj = Task(description=descr)
        obj.creator = self.user
        obj.save()
        url = reverse("tasks:delete", kwargs={'pk': obj.pk})
        self.client.get(url)
        self.assertEquals(Task.objects.count(), 0)

    # OK
    def test_from_delete_not_connect(self):
        reverse("tasks:home")
        descr = 'First description'
        obj = Task(description=descr)
        obj.creator = self.user
        obj.save()
        url = reverse("tasks:delete", kwargs={'pk': obj.pk})
        self.client.get(url)
        self.assertEquals(Task.objects.count(), 1)

    # TODO: edit descr
    def test_from_edit(self):
        self.client.login(
            username=self.username,
            password=self.password)

        reverse("tasks:home")
        descr = 'First description'
        obj = Task(description=descr)
        obj.creator = self.user
        obj.save()

        descrtest = 'Test Description'
        url = reverse("tasks:update", kwargs={'pk': obj.pk})
        response = self.client.post(
            url, {"description": descrtest}, follow=True)
        self.assertEquals(Task.objects.count(), 1)
        self.assertIn(descrtest.encode(), response.content)

    # TODO: edit status
    def test_from_status(self):
        self.client.login(
            username=self.username,
            password=self.password)

        reverse("tasks:home")
        descr = 'First description'
        obj = Task(description=descr)
        obj.creator = self.user
        obj.save()

        status = 'D'
        url = reverse("tasks:update", kwargs={'pk': obj.pk})
        response = self.client.post(
            url, {"status": status}, follow=True)
        self.assertEquals(Task.objects.count(), 1)
        self.assertIn(status.encode(), response.content)
