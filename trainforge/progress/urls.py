from django.urls import path
from . import views

urlpatterns = [
    path('', views.progress_view, name='progress'),
    path('search-clients/', views.search_clients, name='search_clients'),
    path('client-plans/<int:client_id>/', views.client_plans, name='client_plans'),
    path('plan-exercises/<int:plan_id>/<int:client_id>/', views.plan_exercises, name='plan_exercises'),
    path('log/', views.log_progress, name='log_progress'),
]