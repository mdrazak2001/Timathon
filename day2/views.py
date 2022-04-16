import imp
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from base.models import *


def day2(request):
    context = {}
    return render(request, 'day2/day2.html', context)
