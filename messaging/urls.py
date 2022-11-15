from django.urls import path

from . import views

urlpatterns = [
    path('', views.messages_view, name='messages', kwargs={'folder': 'received'}),
    path('sent/', views.messages_view, name='messages_sent', kwargs={'folder': 'sent'}),
    path('create/', views.messages_create, name='messages_create'),
]