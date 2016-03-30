#coding: utf8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from authentication.forms import RegisterAppForm


@login_required
def register_app(request):
    form = RegisterAppForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.save(commit=True)
            return render(request, 'register.html', context={'form': form, 'instance': form.instance})
    return render(request, 'register.html', context={'form': form})
