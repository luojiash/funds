from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from . import views
from .settings import STATICFILES_DIRS

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^accounts/login/$', views.login),
    (r'^accounts/logout/$', views.logout),
    (r'^accounts/changepw/$', views.changepw),
    (r'^home/$', views.home),

    url(r'^funds/', include('funds.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':STATICFILES_DIRS}),
)
