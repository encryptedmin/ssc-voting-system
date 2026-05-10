from django.urls import path
from . import views

urlpatterns = [
    path('candidates/', views.candidate_list, name='candidate_list'),
]