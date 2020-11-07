from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/new', views.CreateGroupView.as_view(), name='group_create'),
    path('groups/<group_id>', views.group_view, name='group_view'),
    path('inv/<str:url>/', views.accept_or_decline_invitation, name='aod_invitation'), # aor = accept or decline
]
