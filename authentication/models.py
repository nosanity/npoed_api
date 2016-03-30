# coding: utf8

from django.db import models
from django.contrib.auth.models import User
from django.utils import crypto


class RegisteredApp(models.Model):
    url = models.URLField(verbose_name=u'URL приложения')
    app_id = models.CharField(max_length=8, unique=True)
    secret = models.CharField(max_length=16)
    user = models.ForeignKey(User, verbose_name=u'Пользователь', related_name='apps')

    def save(self, **kwargs):
        if not self.id:
            app_id = self.generate_id()
            while RegisteredApp.objects.filter(app_id=app_id).exists():
                app_id = self.generate_id()
            self.app_id = app_id
            self.secret = self.generate_secret()
        super(self.__class__, self).save(**kwargs)

    def generate_id(self):
        return crypto.get_random_string(8, '0123456789')

    def generate_secret(self):
        return crypto.get_random_string(16, '0123456789abcdef')

    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name = u'Зарегистрированное приложение'
        verbose_name_plural = u'Зарегистрированные приложения'
