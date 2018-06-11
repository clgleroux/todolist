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
        url = reverse('home')
        response = self.client.get(url)
        self.assertIn(descr1.encode(), response.content)
        self.assertIn(descr2.encode(), response.content)
