from django.urls import path, re_path

from . import views

app_name = 'football'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tournaments/', views.TournamentsView.as_view(), name='tournaments'),
    re_path(r'^tournaments/(?P<id>[0-9]{1,3})/', views.tournament_single),
    path('create-tournament/', views.form_view, name='create_tournament'),
]
