from django.urls import path

from register import views

urlpatterns = [
    path('', views.CheckPhoneView.as_view(), name='check-phone'),
    path('sign-in', views.SignInView.as_view(), name='sign-in'),
]