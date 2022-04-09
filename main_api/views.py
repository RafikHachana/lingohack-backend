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
from .tts import *

# from rest_framework.authtoken.models import Token



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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def get_categories(request):
    result = []
    objects = Category.objects.all()

    for i in objects:
        result.append({
            'id': str(i.Id),
            'name': i.name
        })

    return HttpResponse(json.dumps(result), content_type="application/json")