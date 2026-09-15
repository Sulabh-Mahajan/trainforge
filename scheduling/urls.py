from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('edit/<int:pk>/',   views.edit_appointment,   name='edit_appointment'),
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
]