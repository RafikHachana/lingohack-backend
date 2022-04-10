import json

from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import *
from .text_speech import *

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np

# from rest_framework.authtoken.models import Token

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.

@csrf_exempt
def login_request(request):
    response_data = {}
    if request.method == 'POST':
        # form = AuthenticationForm(request.POST)
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            response_data["status"] = 1
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data["status"] = 0
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)


def logout_request(request):
    logout(request)
    return HttpResponse(json.dumps({'status': 1}), content_type="application/json")


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def current_user(request, format=None):
    try:
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
    except:
        content = {
            'user': None,  # `django.contrib.auth.User` instance.
            'auth': None,  # None
        }
    return HttpResponse(json.dumps(content),content_type="application/json" )


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def get_questions(request):
    data = json.loads(request.body)

    number_of_questions = data.get('number_of_questions')
    source_language = data['source_language']

    # text or speech
    mode = data['mode']

    category_id = data['category_id']


    text_source = Text.objects.filter(language=source_language, category__Id=category_id).order_by('?')[:number_of_questions]
    # Joining the tables
    result = []
    for text in text_source:
        entry = {
            'source': str(text),

            # If the source text is English
            'translation': list(map(lambda x: str(x.russianText) if source_language=="english" else str(x.englishText), 
                Translation.objects.filter(englishText__Id=text.Id).select_related("russianText").all()))
        }

        # If the source text is Russian
        if source_language == 'russian':
            entry['translation'] = list(map(lambda x: str(x.russianText) if source_language=="english" else str(x.englishText), 
                Translation.objects.filter(russianText__Id=text.Id).select_related("englishText").all()))

        result.append(entry)

    if mode == "speech":
        for entry in result:
            source_audio = english_tts(entry["source"]) if source_language == "english" else russian_tts(entry['source'])
            entry['source_audio'] = source_audio

    return HttpResponse(json.dumps(result),content_type="application/json")





@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def get_categories(request):
    result = []
    objects = Category.objects.all()

    for i in objects:
        result.append({
            'id': str(i.Id),
            'name': i.name
        })

    return HttpResponse(json.dumps(result), content_type="application/json")

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def check_speech(request):
    data = json.loads(request.body)

    language = data['language']
    audio_bytes = data['speech'].encode()
    translations = data['translations']

    result = False


    speech_text = english_stt(audio_bytes) if language == 'english' else russian_stt(audio_bytes)

    for translation in translations:
        if speech_text == translation:
            result = True
            break

    return HttpResponse(json.dumps({"result": result}), content_type="application/json")

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def predict_next_word(request):
    data = json.loads(request.body)
    sequence = data['text']
    inputs = tokenizer(sequence, return_tensors="pt")
    inputs_ids = inputs["inputs_ids"]
    for id in inputs_ids[0]:
        word = tokenizer.decode(id)

    with torch.no_grad():
        logits = model(**inputs).logits[:, -1, :]

    predicted_id = torch.argmax(logits).item()
    predicted_word = tokenizer.decode(predicted_id)
    
    result = {
        "predicted_word" : predicted_word
    }

    return HttpResponse(json.dumps(result), content_type="application/json")

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def get_videos(request):
    data = json.loads(request.body)
    
    accent_id = data.get("accent_id")
    category_id = data.get("category_id")

    result = Video.objects.filter(category__Id=category_id, accent__Id=accent_id).values()

    return HttpResponse(json.dumps(result), content_type="application/json")

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def get_accents(request):
    result = []
    objects = Accent.objects.all()

    for i in objects:
        result.append({
            'id': str(i.Id),
            'name': i.name
        })

    return HttpResponse(json.dumps(result), content_type="application/json")

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def add_video(request):
    data = json.loads(request.body)
    
    new_video = Video(
        link=data['link'],
        category=Category.objects.filter(Id=data['category_id'])[0],
        accent=Accent.objects.filter(Id=data['accent_id'])[0],
        description=data.get("description"),
        speaker_name=data.get('speaker_name'),
        title=data.get("title")

    )

    new_video.save()

    return HttpResponse(json.dumps({"success": 1}), content_type="application/json")