# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import defaultdict
from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.decorators import login_required
from django.forms import SelectDateWidget, modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic.list import ListView

from employees.decorators import admin_staff_required
from employees.forms import CheckGroupForm, CheckTaskForm, ChecksForm, ClientForm, ShiftForm
from permission import get_user_permission_object
from sanitytask.forms import CheckForm
from sanitytask.models import CheckTask, Client, Shift, Check, CheckGroup
from .sccalendar import ContestCalendar


# Mixin to redirect in login link for not authenticated user
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class ScheduleListView(LoginRequiredMixin, ListView):
    template_name = 'sanitytask_new/schedule_user.html'
    model = Shift

    def get_context_data(self, **kwargs):
        data = super(ScheduleListView, self).get_context_data(**kwargs)
        perm = get_user_permission_object(user=self.request.user)
        shifts = perm.get_shift(self.request.user)
        qs_shift = defaultdict(set)
        for el in shifts:
            qs_shift[el.checkgroup.client] = perm.get_shift_comp(self.request.user, el.checkgroup.client)
        check = self.get_queryset()
        data['check'] = check
        data['qs_shift'] = dict(qs_shift)
        return data


class DashboardListView(LoginRequiredMixin, ListView):
    template_name = 'sanitytask_new/dashboard.html'
    model = Check

    def post(self, request, *args, **kwargs):
        self.object_list = None
        pa_formset = self.get_context_data()['pa_formset']
        if pa_formset.is_valid():
            for form_ in pa_formset:
                if form_.is_valid():
                    form_.save()
        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        data = super(DashboardListView, self).get_context_data(**kwargs)
        perm = get_user_permission_object(self.request.user)
        t_check = perm.get_check(self.request.user, datetime.today())
        y_check = perm.get_check(self.request.user, datetime.today() - timedelta(1))
        check_formset = modelformset_factory(Check, form=CheckForm, extra=0,
                                             fields=['check_task', 'result', 'comment', 'hidden_result'],
                                             can_delete=False)
        if self.request.POST:
            pa_formset = check_formset(self.request.POST,
                                       queryset=t_check,
                                       prefix='pa')
        else:
            pa_formset = check_formset(queryset=t_check, prefix='pa')
        data = {'y_check': y_check,
                'pa_formset': pa_formset,
                'perm': perm.has_perm()}
        return data


class ScheduleListViewAdmin(LoginRequiredMixin, ListView):
    template_name = 'sanitytask_new/schedule_admin.html'
    model = Shift

    def get_context_data(self, **kwargs):
        field1 = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))
        data = super(ScheduleListViewAdmin, self).get_context_data(**kwargs)
        perm = get_user_permission_object(user=self.request.user)
        shifts = perm.get_empty_shift()
        data['field1'] = field1
        data['shifts'] = shifts
        return data


@login_required()
def check_calendar(request, year_id=datetime.today().year, month_id=datetime.today().month,
                   day_id=datetime.today().day):
    def named_month(month_number):
        """
        Return the name of the month, given the month number
        """
        return datetime(1900, month_number, 1).strftime('%B')

    """
    Show calendar of events for specified month and year
    """
    year = int(year_id)
    month = int(month_id)
    day = int(day_id)
    perm = get_user_permission_object(user=request.user)
    calendar = ContestCalendar().formatmonth(year, month, request.user)
    prev_year = year
    prev_month = month - 1
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1
    next_year = year
    next_month = month + 1
    if next_month == 13:
        next_month = 1
        next_year = year + 1
    check = perm.get_date_check(request.user, year, month, day)

    context = {'calendar': mark_safe(calendar),
               'day': day,
               'month': month,
               'month_name': named_month(month),
               'year': year,
               'prev_month': prev_month,
               'prev_month_name': named_month(prev_month),
               'prev_year': prev_year,
               'next_month': next_month,
               'next_month_name': named_month(next_month),
               'next_year': next_year,
               'check': check
               }

    return render(request, 'sanitytask/calendar.html', context)


@login_required()
@admin_staff_required
def checkgroup_list(request):
    context = {'pa_formset': CheckGroup.objects.all()}
    return render(request, 'checkcreator/checkgroup/checkgroups.html', context)


@login_required()
@admin_staff_required
def checkgroup_add(request):
    if request.method == 'POST':
        chg_form = CheckGroupForm(request.POST)
        if chg_form.is_valid():
            chg_form.save()
            return HttpResponseRedirect(reverse('checkgroups'))
    else:
        chg_form = CheckGroupForm()
    return render(request, 'checkcreator/add.html', {"chg_form": chg_form})


@login_required()
@admin_staff_required
def checktask_list(request):
    context = {'pa_formset': CheckTask.objects.all()}
    return render(request, 'checkcreator/checktask/checktasks.html', context)


@login_required()
@admin_staff_required
def checktask_add(request):
    if request.method == 'POST':
        chg_form = CheckTaskForm(request.POST)
        if chg_form.is_valid():
            chg_form.save()
            return HttpResponseRedirect(reverse('checktask_list'))
    else:
        chg_form = CheckTaskForm()
    return render(request, 'checkcreator/add.html', {"chg_form": chg_form})


@login_required()
@admin_staff_required
def check_list(request):
    context = {'pa_formset': Check.objects.all()}
    return render(request, 'checkcreator/check/checks.html', context)


@login_required()
@admin_staff_required
def check_add(request):
    if request.method == 'POST':
        chg_form = ChecksForm(request.POST)
        if chg_form.is_valid():
            chg_form.save()
            return HttpResponseRedirect(reverse('check_list'))
    else:
        chg_form = ChecksForm()
    return render(request, 'checkcreator/add.html', {"chg_form": chg_form})


@login_required()
@admin_staff_required
def client_list(request):
    context = {'pa_formset': Client.objects.all()}
    return render(request, 'checkcreator/client/clients.html', context)


@login_required()
@admin_staff_required
def client_add(request):
    if request.method == 'POST':
        chg_form = ClientForm(request.POST)
        if chg_form.is_valid():
            chg_form.save()
            return HttpResponseRedirect(reverse('client_list'))
    else:
        chg_form = ClientForm()
    return render(request, 'checkcreator/add.html', {"chg_form": chg_form})


@login_required()
@admin_staff_required
def shift_list(request):
    context = {'pa_formset': Shift.objects.all()}
    return render(request, 'checkcreator/shift/shifts.html', context)


@login_required()
@admin_staff_required
def shift_add(request):
    if request.method == 'POST':
        chg_form = ShiftForm(request.POST)
        if chg_form.is_valid():
            chg_form.save()
            return HttpResponseRedirect(reverse('shift_list'))
    else:
        chg_form = ShiftForm()
    return render(request, 'checkcreator/add.html', {"chg_form": chg_form})
