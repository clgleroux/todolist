# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Task


from django.shortcuts import redirect
from django.urls import reverse
from django.test import TestCase
from django.test import Client

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
