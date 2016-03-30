# coding: utf8

from django.contrib import admin
from authentication.models import RegisteredApp


@admin.register(RegisteredApp)
class RegisteredAppAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'secret', 'url')
    readonly_fields = ('secret', )
