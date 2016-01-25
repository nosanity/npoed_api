# coding: utf8

from django.conf import settings
import requests
from rest_framework.views import APIView, Response


class CourseListView(APIView):
    """
    Список всех сессий курсов в plp

    * GET /api/course_structure/v0/courses/

    или отдельные сессии

    * GET /api/course_structure/v0/courses/?course_id={course_id1},{course_id2}

    """

    def get(self, request, *args, **kwargs):
        """
        ---
        parameters:
        - name: course_id
          description: id курса в виде course-v1:university+course+course_run (например, course-v1:urfu+PHILS+spring_2015)
          required: false
          type: string
          paramType: form
        - name: page
          description: страница с результатами
          paramType: form
          required: false
          type: integer
        """
        url = settings.PLP_URL
        path = request._request.get_full_path()
        resp = requests.get(url + path)
        return Response(resp.json())
