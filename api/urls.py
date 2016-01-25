# coding: utf8

from django.conf.urls import include, url
from api.views import CourseListView


urlpatterns = [
    url('^course_structure/v0/courses/?$', CourseListView.as_view(), name='get-course-list'),
]