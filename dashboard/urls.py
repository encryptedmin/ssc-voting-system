from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path(
        'admin-dashboard/elections/create/',
        views.election_create,
        name='election_create'
    ),
    path(
        'admin-dashboard/elections/<int:election_id>/edit/',
        views.election_update,
        name='election_update'
    ),
    path(
        'admin-dashboard/elections/<int:election_id>/delete/',
        views.election_delete,
        name='election_delete'
    ),
    path(
        'admin-dashboard/voters/<int:voter_id>/<str:action>/',
        views.voter_action,
        name='voter_action'
    ),
    path('voter-dashboard/', views.voter_dashboard, name='voter_dashboard'),
]
