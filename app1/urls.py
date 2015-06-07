from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    (r'^add/$', views.add_book.as_view()),
    (r'^$', views.show_books.as_view()),
    (r'^authors/$', views.show_authors.as_view()),
    (r'^search/$', views.search),

)
