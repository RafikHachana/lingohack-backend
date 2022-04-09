from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),\
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('current_user', views.current_user, name="current_user"),
    path('get_categories', views.get_categories, name="get_categories"),
    path('get_questions', views.get_questions, name="get_questions"),
    path('check_speech', view=views.check_speech, name="check_speech"),
    path('get_next_word', views.predict_next_word, name="get_next_word"),
    path("get_videos", views.get_videos, name="get_videos"),
    path("add_video", views.add_video, name="add_video"),\
    path("get_accents", views.get_accents, name="get_accents")
]