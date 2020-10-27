from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/groups/', views.GroupListView.as_view(), name='group_list'),
]
