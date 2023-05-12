from django.urls import path

from register import views

urlpatterns = [
    path('', views.CheckPhoneView.as_view(), name='check-phone'),
    path('sign-in', views.SignInView.as_view(), name='sign-in'),
    path('sign-up/step/1', views.SignUpStep1View.as_view(), name='sign-up-step-1'),
    path('sign-up/step/2', views.SignUpStep2View.as_view(), name='sign-up-step-2'),
]