# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Task

from django.urls import reverse
from django.test import TestCase

# Create your tests here.


class TestTask(TestCase):

    def test_list_view(self):
        descr1 = 'First description'
        descr2 = 'Second description'
        Task(description=descr1).save()
        Task(description=descr2).save()
        url = reverse('tasks:home')
        response = self.client.get(url)
        self.assertIn(descr1.encode(), response.content)
        self.assertIn(descr2.encode(), response.content)

    def test_form_exists(self):
        create = reverse("tasks:home")
        response = self.client.get(create)
        self.assertEquals(response.status_code, 200)

    def test_form_valid(self):
        create = reverse("tasks:home")
        response = self.client.post(create, {"description": "First todo"})
        self.assertEquals(response.status_code, 302)

    def test_form_invalid(self):
        create = reverse("tasks:home")
        response = self.client.post(create, {})
        self.assertEquals(response.status_code, 400)
