from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clients/add/',views.add_client,name='add_client'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('plan/<int:assignment_id>/end/',   views.end_plan,name='end_plan'),
    path('progress/<int:exercise_id>/client/<int:client_id>/add/', views.add_progress, name='add_progress'),
    path('clients/<int:client_id>/assign-plan/', views.assign_plan_to_client, name='assign_plan_to_client'),
    path('clients/<int:client_id>/edit/', views.edit_client, name='edit_client'),
    path('clients/<int:client_id>/archive/', views.archive_client, name='archive_client'),
]

