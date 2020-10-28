from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/new', views.CreateGroupView.as_view(), name='group_create'),
]
