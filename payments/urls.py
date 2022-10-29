from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='payments_home'),
    path('config/', views.stripe_config),
    path('award/<str:tier>/<str:price_id>/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view(), name='payments_success'),
    path('cancelled/', views.CancelledView.as_view(), name='payments_cancelled'),
    path('webhook/', views.stripe_webhook),
]