from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('group/new', views.GroupCreateView.as_view(), name='new_group'),
    path('group/<slug:slug>/', views.GroupDetailView.as_view(), name='group_detail'),
    path('login/', views.Login.as_view(), name='login'),
    path('', views.TemplateView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
