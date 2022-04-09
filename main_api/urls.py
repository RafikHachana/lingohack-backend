from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),\
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('current_user', views.current_user, name="current_user"),
    path('get_categories', views.get_categories, name="get_categories"),
    path('get_questions', views.get_questions, name="get_questions")
]