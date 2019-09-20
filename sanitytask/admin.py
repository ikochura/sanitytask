# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from sanitytask.models import CheckGroup, CheckTask, Check, Shift, Client


@admin.register(CheckTask)
class CheckTaskAdmin(admin.ModelAdmin):
    list_display = ['check_group', 'name_task']
    list_filter = ['check_group__name']


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ['check_task', 'user']
    list_filter = ['result', 'date', 'check_task']


@admin.register(CheckGroup)
class CheckGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'client']
    list_filter = ['client']


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    fields = ('user', 'checkgroup', ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'))
    list_filter = ['checkgroup__client__name', 'user__username', 'checkgroup__name']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    filter_horizontal = ('user',)
