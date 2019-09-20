# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
import datetime

from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=250, default='')
    user = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('all_companies', 'Can view all companies'),
            ('current_companies', 'Can view current companies'),
        )


class CheckGroup(models.Model):
    name = models.CharField(max_length=60)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False)

    def __unicode__(self):
        return self.client.name + '/' + self.name


class CheckTask(models.Model):
    name_task = models.CharField(max_length=250)
    check_group = models.ForeignKey(CheckGroup)

    def __unicode__(self):
        return self.name_task + '/' + self.check_group.name


class Check(models.Model):
    date = models.DateField()
    result = models.BooleanField(default=False)
    hidden_result = models.BooleanField()
    user = models.ForeignKey(User)
    check_task = models.ForeignKey(CheckTask, on_delete=models.CASCADE, blank=False)
    comment = models.TextField(max_length=1000, default='', blank=True)

    def __unicode__(self):
        return self.check_task.name_task

    def get_done(self):
        if self.result:
            return 'Done'

    def get_class(self):
        if self.result == self.hidden_result is True:
            return 'alert alert-success'
        if self.result is False and self.hidden_result is True:
            return 'alert alert-danger'
        else:
            return 'alert alert-danger'


class Shift(models.Model):
    user = models.ForeignKey(User)
    checkgroup = models.ForeignKey(CheckGroup, on_delete=models.CASCADE)
    mon = models.BooleanField(default=False)
    tue = models.BooleanField(default=False)
    wed = models.BooleanField(default=False)
    thu = models.BooleanField(default=False)
    fri = models.BooleanField(default=False)
    sat = models.BooleanField(default=False)
    sun = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('view_all', 'view_all'),
            ('view_current', 'view_current'),
        )

    def __unicode__(self):
        return 'Shift {} to check group {} of client {}'.format(self.user, self.checkgroup.name,
                                                                self.checkgroup.client.name)

    def shift_in_days(self):
        days_list = [self.mon, self.tue, self.wed, self.thu, self.fri, self.sat, self.sun]
        if days_list[datetime.datetime.today().weekday()] == 1:
            return True

    def next_shift(self):
        days_list = [self.mon, self.tue, self.wed, self.thu, self.fri, self.sat, self.sun]
        n = datetime.datetime.today().weekday()
        if True not in days_list:
            return "Yod don't have a shift"
        else:
            if n == 6:
                idx = days_list.index(True)
                return 'You next shift {} at {}'.format(self.checkgroup, list(calendar.day_name)[idx])
            elif n in range(0, 6) and True in days_list[n + 1:]:
                idx = days_list[n + 1:].index(True) + n + 1
                return 'You next shift {} at {}'.format(self.checkgroup, list(calendar.day_name)[idx])
            else:
                idx = days_list.index(True)
                return 'You next shift {} at {}'.format(self.checkgroup, list(calendar.day_name)[idx])

    def get_checkgroup(self):
        return self.checkgroup
