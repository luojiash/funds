from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = patterns('',

    (r'^me/$', views.me),
    (r'^me/update/(?P<pk>\d+)$', login_required(views.me_update.as_view())),

    (r'^record/$', login_required(views.record.as_view())),
    (r'^record/assum/create/$', login_required(views.assum_create.as_view())),
    (r'^record/income/create/$', login_required(views.income_create.as_view())),
    (r'^record/other/create/$', login_required(views.other_create.as_view())),

    (r'^record/assum/$', login_required(views.assum.as_view())),
    (r'^record/income/$', login_required(views.income.as_view())),
    (r'^record/other/$', login_required(views.other.as_view())),

    (r'^record/assum/update/(?P<pk>\d+)$', login_required(views.assum_update.as_view())),
    (r'^record/income/update/(?P<pk>\d+)$', login_required(views.income_update.as_view())),
    (r'^record/other/update/(?P<pk>\d+)$', login_required(views.other_update.as_view())),

    (r'^account/$', login_required(views.account.as_view())),
    (r'^account/deposit/create/$', login_required(views.deposit_create.as_view())),
    (r'^account/loan/create/$', login_required(views.loan_create.as_view())),

    (r'^account/deposit/delete/(?P<pk>\w+)$', login_required(views.deposit_delete.as_view())),
    (r'^account/loan/delete/(?P<pk>\w+)$', login_required(views.loan_delete.as_view())),
    (r'^account/deposit/update/(?P<pk>\w+)$', login_required(views.deposit_update.as_view())),
    (r'^account/loan/update/(?P<pk>\w+)$', login_required(views.loan_update.as_view())),


)
