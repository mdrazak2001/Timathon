from playsound import playsound
import enchant
import datetime
from ast import pattern
from tkinter import *
import tkinter.scrolledtext as scrolledtext
import email
from warnings import catch_warnings
from django.shortcuts import render
from matplotlib.style import context
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import Score
from django.contrib.auth.decorators import login_required


def home(request):
    context = {}
    name = request.user
    if request.user.is_authenticated:
        score = Score.objects.get(of=name)
        temp_score = int(request.GET.get('score', 0))
        day = int(request.GET.get('day', 0))
        try:
            if day == 1 and not score.day1:
                score.day1 = True
                score.score += temp_score
            if day == 2 and not score.day2:
                score.day2 = True
                score.score += temp_score
            if day == 3 and not score.day3:
                score.day3 = True
                score.score += temp_score
        except:
            pass
        score.save()
        context['score'] = score.score
    return render(request, 'base/home.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Dosent Exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    page = 'login'
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    if request.method == 'POST':
        # form = CustomUserCreationForm(request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     Score.objects.create(of=user, score=0)
        #     return redirect('home')
        # else:
        #     messages.error(request, 'An Error Occured during registration')
        username = request.POST['username']
        mail = request.POST['email']
        p1 = request.POST['password1']
        p2 = request.POST['password2']
        print(p1, p2)
        if(p1 == p2):
            if User.objects.filter(email=email).first() is not None:
                messages.add_message(
                    request, messages.INFO, 'email name taken')
                render(request, 'base/login_register.html')
            elif User.objects.filter(username=username).first() is not None:
                messages.add_message(
                    request, messages.INFO, 'User name taken')
                render(request, 'base/login_register.html')
            else:
                user_ob = User.objects.create(
                    username=username, email=mail)
                user_ob.set_password(p1)
                Score.objects.create(of=user_ob, score=0)
                user_ob.save()
            return redirect('login')
        else:
            messages.add_message(
                request, messages.INFO, 'Passwords Dont Match')

    else:
        form = CustomUserCreationForm()
    return render(request, 'base/login_register.html', {'form': form})


score = 0
accepted_words = []


@login_required(login_url='login')
def dayone(request):
    context = {}

    done = 'false'
    user = request.user
    sc = Score.objects.get(of=user)
    if sc.day1:
        done = 'true'
    context['done'] = done

    chars = ['e', 't', 'a', 'i', 'n', 'o', 's',
             'h', 'r', 'd', 'l', 'u', 'c', 'm', 'f', 'p']
    context['chars'] = chars
    context['bool'] = 'true'
    options = []
    if request.method == 'POST':
        options = request.POST.getlist("select")
        options = options[:8]
        char_options = []
        for o in options:
            char_options.append(chars[int(o)])
        char_options = ' '.join(map(str, char_options))
        req = 'chars=' + char_options

        '''Set Target Time For task'''
        current_datetime = datetime.datetime.now()
        hh = current_datetime.hour
        mm = current_datetime.minute
        ss = current_datetime.second + 90
        req = req + '&hh=' + str(hh)
        req = req + '&mm=' + str(mm)
        req = req + '&ss=' + str(ss)
        score = 0
        accepted_words = []

        return redirect('/day1game/?' + f'{req}')

    return render(request, 'base/day1.html', context)


@login_required(login_url='login')
def day1game(request):
    context = {}
    ''' Get 'get' Parameters '''
    chars = request.GET.get('chars', -1)
    hh = int(request.GET.get('hh', -1))
    mm = int(request.GET.get('mm', -1))
    ss = int(request.GET.get('ss', -1))

    '''Chosen Pattern Recognition of give chars'''
    p = ''
    for c in chars:
        if c != ' ':
            p += c + '*'
    context['pattern'] = p
    new_chars_list = chars.split()
    context['chars'] = new_chars_list
    new_chars_list.append("backspace")
    new_chars_list.append("done")

    '''Target Time Task Completion'''
    context['hh'] = hh
    context['mm'] = mm
    context['ss'] = ss
    global score
    global accepted_words
    if request.method == 'POST':
        word = request.POST['word']
        print(valid(word, chars))
        if valid(word, chars):
            score += len(word)
            accepted_words.append(word)
            playsound(r'static\success.wav')
        else:
            playsound(r'static\fail.mp3')
        print(word)
    context['score'] = score

    return render(request, 'base/day1game.html', context)


def valid(word, chars):
    d = enchant.Dict("en_US")
    for c in word:
        ok = False
        for l in chars:
            if c == l:
                ok = True
                break
        if not ok:
            return False
    for w in accepted_words:
        if w == word:
            return False
    return d.check(word) and len(word) >= 3 and len(word) <= 8
