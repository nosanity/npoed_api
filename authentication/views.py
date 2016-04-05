#coding: utf8

import base64
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from authentication.forms import RegisterAppForm
from authentication.models import RegisteredApp


@login_required
def register_app(request):
    form = RegisterAppForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.save(commit=True)
            return render(request, 'register.html', context={'form': form, 'instance': form.instance})
    return render(request, 'register.html', context={'form': form})


class AppAuthentication(BaseAuthentication):
    def authenticate(self, request):
        app_id, secret = request.META.get('HTTP_X_ID'), request.META.get('HTTP_X_SECRET')
        if RegisteredApp.objects.filter(app_id=app_id, secret=secret).exists():
            return True, True
        raise AuthenticationFailed()

    def authenticate_header(self, request):
        return 'Missing or wrong credentials provided'


class PingView(APIView):
    authentication_classes = (AppAuthentication, )

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


def get_auth_header():
    auth = base64.b64encode('{}:{}'.format(settings.SOCIAL_AUTH_NPOEDSSO_KEY, settings.SOCIAL_AUTH_NPOEDSSO_SECRET))
    return {'Authorization': 'auth %s' % auth}


class RegistrationView(APIView):
    permission_classes = []
    authentication_classes = []
    request_url = '{}{}'.format(settings.SSO_NPOED_URL, '/registration-api/')

    def get(self, request, *args, **kwargs):
        try:
            r = requests.get(self.request_url, headers=get_auth_header())
            return Response(r.json())
        except IOError:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def post(self, request, *args, **kwargs):
        try:
            r = requests.post(self.request_url, data=request.DATA, headers=get_auth_header())
            return Response(r.json() if r.content else '', status=r.status_code)
        except IOError:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
