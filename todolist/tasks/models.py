# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class TASK(models.Model):
    description = models.TextField(max_length=240)
    NEW = 'N'
    PENDING = 'P'
    DONE = 'D'
    STATUS_CHOICES = (
        (NEW, 'New'),
        (PENDING, 'Pending'),
        (DONE, 'Done'),
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=NEW,
    )

    def __str__(self):
        return '{} - {}'.format(self.description, self.status)

    def get_my_status():
        # you place some logic here
        return TASK.STATUS_CHOICES
