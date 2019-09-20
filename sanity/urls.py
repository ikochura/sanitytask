"""sanity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

from employees.views import MyProfile, profile_edit, change_pass
from sanitytask.views import check_calendar, ScheduleListViewAdmin, DashboardListView, ScheduleListView, \
    checkgroup_list, checkgroup_add, checktask_list, checktask_add, check_list, check_add, client_list, client_add, \
    shift_list, shift_add

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^accounts/', include('django.contrib.auth.urls')),
                  url(r'^calendar/([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})/$', check_calendar, name='calendar_day'),
                  url(r'^calendar/$', check_calendar, name='check_calendar'),
                  url(r'^shift/admin/$', ScheduleListViewAdmin.as_view(), name='schedule-admin'),
                  url(r'^dashboard/$', DashboardListView.as_view(), name='dashboard'),
                  url(r'^shift/$', ScheduleListView.as_view(), name='schedule'),
                  url(r'^employee/', include('employees.urls')),
                  url(r'^profile/$', MyProfile.as_view(), name="my_profile"),
                  url(r'^profile/edit/$', profile_edit, name="profile_edit"),
                  url(r'^profile/pass/$', change_pass, name="change_pass"),

                  url(r'^checkgroups/$', checkgroup_list, name="checkgroups"),
                  url(r'^checkgroups/add/$', checkgroup_add, name="checkgroup_add"),

                  url(r'^checktasks/$', checktask_list, name="checktask_list"),
                  url(r'^checktasks/add/$', checktask_add, name="checktask_add"),

                  url(r'^check/$', check_list, name="check_list"),
                  url(r'^check/add/$', check_add, name="check_add"),

                  url(r'^client/$', client_list, name="client_list"),
                  url(r'^client/add/$', client_add, name="client_add"),
                  url(r'^shifts/$', shift_list, name="shift_list"),
                  url(r'^shifts/add/$', shift_add, name="shift_add"),
                  url(r'^$', RedirectView.as_view(url='dashboard')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
