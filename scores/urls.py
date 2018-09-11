# -*- coding:utf-8 -*-
from django.urls import path, re_path

from . import views

app_name = 'scores'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'login/$', views.login, name='login'),
    re_path(r'register/$', views.register, name='register'),
    path('user/profile/', views.profile, name='profile'),
    path('user/profile/update/', views.profile_update, name='profile_update'),
    path('user/pwd_change/', views.pwd_change, name='pwd_change'),
    path('logout/', views.logout, name='logout'),
    path('user/score/', views.score, name='score'),
    path('user/score/<int:schedule_term>/', views.score_detail, name='score_detail'),
    path('user/score/manage/', views.score_manage, name='score_manage'),
    path('user/score/manage/<int:assignment_id>/', views.score_manage_detail, name='score_manage_detail'),
    path('user/score/manage/<int:assignment_id>/input/', views.score_manage_input, name='score_manage_input'),
    path('user/assignment/manage/', views.assignment_manage, name='assignment_manage'),
    path('user/assignment/manage/update/<int:assignment_id>/', views.assignment_update, name='assignment_update'),

    # path('user/score/manage/<int:assignment_id>/save/', views.score_manage_save, name='score_manage_save'),
]