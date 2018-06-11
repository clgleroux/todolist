# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import TASK

from django.test import TestCase

# Create your tests here.


class TestTask(TestCase):

    def test_creation(self):
        description = 'Je suis la premiere tache'
        obj = TASK.objects.create(description=description)
        id = obj.id
        self.assertEquals(len(obj.status), 1)
        self.assertEquals(obj.status, 'N')
        self.assertEquals(obj.description, description)
        self.assertEquals(obj.id, id)
        self.assertEquals(TASK.objects.all().count(), 1)

    def test_differents(self):
        obj1 = TASK.objects.create(description='Je suis la premiere tache')
        obj2 = TASK.objects.create(description='Je suis la seconde tache')
        self.assertEquals(TASK.objects.all().count(), 2)
        self.assertNotEquals(obj1, obj2)

    def test_status(self):
        obj1 = TASK.objects.create(description='Je suis la premiere tache')
        obj1.status = 'P'
        self.assertEquals(obj1.status, 'P')

    def test_delete(self):
        obj1 = TASK.objects.create(description='Je suis la premiere tache')
        self.assertEquals(TASK.objects.all().count(), 1)
        TASK.objects.all().delete()
        self.assertEquals(TASK.objects.all().count(), 0)
        obj1 = TASK.objects.create(description='Je suis la premiere tache')
        self.assertEquals(TASK.objects.all().count(), 1)
        id = obj1.id
        obj = TASK.objects.get(id=id)
        obj.delete()
        self.assertEquals(TASK.objects.all().count(), 0)

    def test_status_invalid(self):
        obj1 = TASK.objects.create(description='Je suis la premiere tache')
        obj1.status = 'P'
        self.assertEquals(obj1.status, TASK.get_my_status())
