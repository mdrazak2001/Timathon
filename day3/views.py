import sys
from django.shortcuts import redirect, render
from matplotlib.style import context
from pyparsing import line
from base.models import *
from PIL import ImageChops, Image
import numpy as np
import matplotlib.pyplot as plt

score = 0


def day3(request):
    context = {}
    user = request.user
    sc = Score.objects.get(of=user)
    done = 'false'
    global score
    print(score)
    if sc.day3:
        done = 'true'
    context['done'] = done
    mcq = ['1c', '2c', '3b']
    if request.method == 'POST':
        q1 = request.POST['q1']
        q2 = request.POST['q2']
        q3 = request.POST['q3']
        if q1 == mcq[0]:
            score += 2
        if q2 == mcq[1]:
            score += 2
        if q3 == mcq[2]:
            score += 2
        # print(q1, q2, q3, score)
        return redirect('py/')
    return render(request, 'day3/day3.html', context)


cd = 'def solve(word):'


def day3py(request):
    context = {}
    output = ''
    global score
    data1 = data2 = ''
    once_ran = False
    global cd
    if request.method == 'POST' and 'submit' in request.POST:
        code = request.POST['codearea']
        once_ran = True
        cd = code
        with open('input.txt', 'w') as f:
            f.write(code)
        data1 = open('input.txt', 'r').read()
        data2 = open('test.txt', 'r').read()
        data1 += "\n"
        data1 += data2
        code = data1
        try:
            # save incoming
            original_stdout = sys.stdout
            sys.stdout = open('output.txt', 'w')
            exec(code)
            sys.stdout.close()

            sys.stdout = original_stdout
            output = open('output.txt', 'r').read()
            lines = []
            with open('output.txt') as f:
                lines = [line.rstrip('\n') for line in f]
                # print(lines)
            print(lines)
            if lines[0] == 'True' and lines[1] == 'False':
                score += 10
            elif lines[0] == 'True':
                score += 5
            elif lines[1] == 'False':
                score += 5
            else:
                score += 0
            return redirect('/?score='+f'{score}'+'&day=3')
        except Exception as e:
            print(e)

    if request.method == 'POST' and 'tests' in request.POST:
        code = request.POST['codearea']
        once_ran = True
        cd = code
        with open('input.txt', 'w') as f:
            f.write(code)
        data1 = open('input.txt', 'r').read()
        data2 = open('test.txt', 'r').read()
        data1 += "\n"
        data1 += data2
        code = data1
        try:
            # save incoming
            original_stdout = sys.stdout
            sys.stdout = open('output.txt', 'w')
            exec(code)
            sys.stdout.close()

            sys.stdout = original_stdout
            output = open('output.txt', 'r').read()

        except Exception as e:
            output = open('output.txt', 'r').read()
            print(e)
        return redirect('day3py')
        # print('submit')
    output = open('output.txt', 'r').read()
    context['output'] = output

    test1 = 'malayalam'
    test2 = 'geeks'
    context['t1'] = test1
    context['t2'] = test2
    context['code'] = cd
    context['bool'] = once_ran
    return render(request, 'day3/day3py.html', context)


def handle_uploaded_file(f):
    with open(r'static\day2\t.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def match(path1, path2):
    actual_error = 0
    im1 = Image.open(path1)
    x = np.array(im1.histogram())

    im2 = Image.open(path2)
    y = np.array(im2.histogram())

    try:
        if len(x) == len(y):
            error = np.sqrt(((x - y) ** 2).mean())
            error = str(error)[:2]
            actual_error = float(100) - float(error)
        diff = ImageChops.difference(im1, im2).getbbox()
        if diff:
            print("Not Duplicate Image")
            return actual_error
        else:
            print("Duplicate Image")
            return actual_error

    except ValueError as identifier:
        f = plt.figure()
        return actual_error
