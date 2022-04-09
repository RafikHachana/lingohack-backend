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