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
from PIL import ImageChops, Image
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
import sounddevice as sd
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
import re

send = ["521634s321", "918342s321", "241425s321", 's', ""]
i = 0
score = 0


@csrf_exempt
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
        context['score'] = score
        i = i + 1
        s = send[i]
        context['send'] = s
        return render(request, 'day2/day2.html', context)
    context['score'] = score
    context['send'] = s
    return render(request, 'day2/day2.html', context)


# a function that splits the audio file into chunks
# and applies speech recognition

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
