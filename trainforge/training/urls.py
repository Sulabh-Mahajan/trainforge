from django.urls import path
from . import views

urlpatterns = [
    path('plans/',                        views.training_plans, name='training_plans'),
    path('plans/create/',                 views.create_plan,    name='create_plan'),
    path('plans/<int:plan_id>/view/',     views.view_plan,      name='view_plan'),
    path('plans/<int:plan_id>/edit/',     views.edit_plan,      name='edit_plan'),
    path('plans/<int:plan_id>/delete/',   views.delete_plan,    name='delete_plan'),
    path('plans/<int:plan_id>/assign/',   views.assign_plan,    name='assign_plan'),
    path('generate-ai/', views.generate_plan_ai, name='generate_plan_ai'),
]