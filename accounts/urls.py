from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('', views.TemplateView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('accounts/password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('accounts/password_reset/', views.PasswordReset.as_view(), name='password_reset_form'),
    path('accounts/password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
]
