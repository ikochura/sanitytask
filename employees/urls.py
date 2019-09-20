from django.conf.urls import url

from employees.views import employee_list, employee_details, employee_edit, employee_add, employee_delete

urlpatterns = [
    url(r'^$', employee_list, name='employee_list'),
    url(r'^(?P<id>\d+)/details/$', employee_details, name="employee_details"),
    url(r'^(?P<id>\d+)/edit/$', employee_edit, name="employee_edit"),
    url(r'^add/$', employee_add, name="employee_add"),
    url(r'^(?P<id>\d+)/delete/$', employee_delete, name="employee_delete"),
]
