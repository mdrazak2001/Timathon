from pydub.silence import split_on_silence
from pydub import AudioSegment
import os
import pydub
import ftplib
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from base.models import *
import time
from playsound import playsound
import sounddevice as sd
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
import re
from django.contrib.auth.decorators import login_required

send = ["521634s321", "918342s321", "241425s321", 's', ""]
i = 0
score = 0


@csrf_exempt
@login_required(login_url='login')
def day2(request):
    context = {}
    global i
    global send
    global score
    s = send[0]
    done = 'false'
    user = request.user
    sc = Score.objects.get(of=user)
    if sc.day2:
        done = 'true'
    context['done'] = done
    if request.method == 'POST':
        s = send[i]
        op = s[:6]
        ip = record()
        ip = re.sub(r"\s+", "", ip)
        if(op == ip):
            playsound(r'static\success.wav')
            score += 6
        else:
            playsound(r'static\fail.mp3')
        if(s == 's'):
            i = 0
            sc = score
            score = 0
            return redirect('/?score=' + str(sc) + '&day=2')
        context['score'] = score
        i = i + 1
        s = send[i]
        context['send'] = s
        return render(request, 'day2/day2.html', context)
    context['score'] = score
    context['send'] = s
    return render(request, 'day2/day2.html', context)


def record():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # listen for the data (load audio to memory)
        r.adjust_for_ambient_noise(source)
        print("say...")
        audio_data = r.listen(source)
        try:
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
            print(text)
            return text
        except:
            print("srry")
