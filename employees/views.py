# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView

from decorators import admin_staff_required
from employees.forms import UserForm, ProfileForm, PasswordChangeForm
from sanitytask.views import LoginRequiredMixin


@login_required()
@admin_staff_required
def employee_list(request):
    context = {'users': User.objects.filter(groups__name__in=['Users', 'Staff']), 'title': 'Employees'}
    return render(request, 'employee/users_list.html', context)


@login_required()
@admin_staff_required
def employee_details(request, id=None):
    context = {'user': get_object_or_404(User, id=id)}
    return render(request, 'employee/details.html', context)


@login_required()
@admin_staff_required
def employee_add(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            u = user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/add.html', context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        return render(request, 'employee/add.html', context)


@login_required()
@admin_staff_required
def employee_edit(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/edit.html', {"user_form": user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'employee/edit.html', {"user_form": user_form})


@login_required()
@admin_staff_required
def employee_delete(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {'user': user}
        return render(request, 'employee/delete.html', context)


class MyProfile(LoginRequiredMixin, DetailView):
    template_name = 'auth/profile.html'

    def get_object(self, **kwargs):
        return self.request.user


@login_required()
def profile_edit(request):
    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():

            user_form.save()
            return HttpResponseRedirect(reverse('my_profile'))
        else:
            return render(request, 'auth/profile_update.html', {"user_form": user_form})
    else:
        user_form = ProfileForm(instance=request.user)
        return render(request, 'auth/profile_update.html', {"user_form": user_form})


@login_required()
def change_pass(request):
    form = PasswordChangeForm(request.POST or None)
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    re_new_password = request.POST.get("re_new_password")
    if request.POST.get('old_password'):
        if not request.user.check_password('{}'.format(old_password)):
            form.set_old_password_flag()
    if request.POST.get('new_password') and request.POST.get('re_new_password'):
        if not new_password == re_new_password:
            form.set_new_password_flag()
    if form.is_valid():
        request.user.set_password('{}'.format(new_password))
        request.user.save()
        update_session_auth_hash(request, request.user)

        return redirect('my_profile')

    else:
        return render(request, 'auth/profile_update.html', {"user_form": form})
