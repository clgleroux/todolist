# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User


class Task(models.Model):
    description = models.TextField(max_length=240)
    NEW = 'N'
    PENDING = 'P'
    DONE = 'D'
    STATUS_CHOICES = (
        (NEW, _('New')),
        (PENDING, _('Pending')),
        (DONE, _('Done')),
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=NEW,
    )
    creator = models.ForeignKey(
        User,
    )

    def __str__(self):
        if len(self.description) >= 40:
            description = self.description[:40] + '...'
        else:
            description = self.description
        return '{} - {}'.format(description, self.status)
