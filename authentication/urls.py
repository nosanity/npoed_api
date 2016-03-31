# coding: utf8

from django.conf.urls import url
from authentication.views import PingView

urlpatterns = [
    url(r'^register/?$', 'authentication.views.register_app', name='register-app'),
    url(r'^ping/?$', PingView.as_view(), name='ping'),
]
