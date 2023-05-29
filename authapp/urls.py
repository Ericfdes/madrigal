from django.urls import path

from authapp import views

from authapp.forms import *
from authapp import pipeline
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.views.generic import RedirectView
from django.urls import reverse_lazy


urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_register/', views.user_register, name='user_register'),
    path('aspire-policy/', views.policy, name='policy'),

    # path('authenticate_linkedin/', views.authenticate_linkedin, name='authenticate_linkedin'),
    # path('extract_linkedin_data/', views.extract_linkedin_data, name='extract_linkedin_data'),
   
    # path('social-auth/<backend>/', views.extract_user_data_view, name='socialauth_extract_userdata'),
    # path('capture-linkedin-data/<backend>/', pipeline.capture_user_data, name='capture-linkedin'),
    # path('linkedin-login/', views.linkedin_login, name='linkedin_login'),
    

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=UserPasswordResetFormConfirm),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
        
    
    
]
