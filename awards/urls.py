from django.urls import path

from . import views

urlpatterns = [
    path('', views.awards_view, name='awards'),
    path('send/', views.awards_send, name ='awards_send'),
    path('detail/', views.awards_detail, name='awards_detail'),
]