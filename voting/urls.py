from django.urls import path
from . import views

urlpatterns = [

    path(
        'ballot/<int:election_id>/',
        views.ballot_view,
        name='ballot'
    ),

    path(
        'submit-vote/<int:election_id>/',
        views.submit_vote,
        name='submit_vote'
    ),

    path(
        'results/<int:election_id>/',
        views.results_view,
        name='results'
    ),
]