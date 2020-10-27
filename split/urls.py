from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:pk>/groups/', views.GroupListView.as_view(), name='group_list'),
]
