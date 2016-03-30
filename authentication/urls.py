# coding: utf8

from django.conf.urls import url

urlpatterns = [
    url(r'^register/?$', 'authentication.views.register_app', name='register-app'),
]