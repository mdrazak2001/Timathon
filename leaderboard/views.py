from math import floor
from django.shortcuts import render
import sys
from django.shortcuts import redirect, render
from matplotlib.style import context
from pyparsing import line
from base.models import *
from PIL import ImageChops, Image
import numpy as np
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def leaderboard(request):
    context = {}
    users = User.objects.all()
    order = []
    for u in users:
        score = Score.objects.get(of=u)
        order.append((u.username, score.score))
        # print(u.username, score.score)
    order.sort(key=lambda i: i[1], reverse=True)
    names = []
    scores = []
    for o in order:
        names.append(order[0])
        scores.append(order[1])
    context['names'] = names
    context['scores'] = scores
    context['order'] = order
    return render(request, 'leaderboard/home.html', context)


@login_required(login_url='login')
def analysis(request):
    context = {}
    user = request.user
    score = Score.objects.get(of=user)
    tasks = 0
    strin = ''
    # print(avg)
    print(score.of.username)

    if score.day1:
        tasks += 1
    if score.day2:
        tasks += 1
    if score.day3:
        tasks += 1

    if tasks != 3:
        tasks = tasks/3 * 100
    else:
        tasks = 100
    users = User.objects.all()
    tot = 0

    for u in users:
        score = Score.objects.get(of=u)
        # order.append((u.username, score.score))
        tot += score.score
    user = request.user
    score = Score.objects.get(of=user)
    avg = tot / len(users)
    print(avg)
    if score.score > avg:
        # print("hi")
        a = score.score - avg
        a /= score.score
        a *= 100
        a = floor(a)
        strin = 'Your score is ' + \
            str(score.score) + ' ,' + str(a) + '%' + 'Above Average'
    else:
        a = avg - score.score
        a /= 100
        a *= 100
        a = floor(a)
        strin = 'Your score is ' + \
            str(score.score) + ' ,' + str(a) + '%' + 'Below average'
    # user = request.user
    # score = Score.objects.get(of=user)
    context['strin'] = strin
    context['tasks'] = tasks
    return render(request, 'leaderboard/analysis.html', context)
