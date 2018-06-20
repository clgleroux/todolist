from django.conf.urls import url

from tasks.views import (
    home, delete, update
)

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^delete/(?P<pk>[0-9]+)/$', delete, name="delete"),
    url(r'^update/(?P<pk>[0-9]+)/$', update, name="update"),
]
