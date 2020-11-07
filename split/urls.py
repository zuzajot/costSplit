from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginRequest, name='home'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    path('cost/<int:pk>/new/', views.CostCreateView.as_view(), name='cost_new'),
    path('cost/<int:pk>/edit', views.CostEditView.as_view(), name='cost_edit'),
    path('cost/<int:pk>/delete', views.CostDeleteView.as_view(), name='cost_delete'),

    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/new', views.CreateGroupView.as_view(), name='group_create'),
    path('groups/<group_id>', views.group_view, name='group_view'),
    path('inv/<str:url>/', views.accept_or_decline_invitation, name='aod_invitation'), # aod = accept or decline
    path('groups/<int:pk>/delete', views.GroupDeleteView.as_view(), name='group_delete'),
]
