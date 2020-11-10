from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login/', views.login_request, name='home'),
    path('', views.GroupListView.as_view(), name='home'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    path('accounts/password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('accounts/password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('accounts/password_reset/', views.PasswordReset.as_view(), name='password_reset_form'),
    path('accounts/password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),

    path('groups/<group_id>/cost/new/', views.CostCreateView.as_view(), name='cost_new'),
    path('cost/<int:pk>/edit', views.CostEditView.as_view(), name='cost_edit'),
    path('cost/<int:pk>/delete', views.CostDeleteView.as_view(), name='cost_delete'),

    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/new', views.CreateGroupView.as_view(), name='group_create'),
    path('groups/<group_id>', views.group_view, name='group_view'),
    path('groups/<group_id>/payment', views.MakePaymentView.as_view(), name='make_payment'),
    path('inv/<str:url>/', views.accept_or_decline_invitation, name='aod_invitation'), # aod = accept or decline
    path('groups/<int:pk>/delete', views.GroupDeleteView.as_view(), name='group_delete'),
]
