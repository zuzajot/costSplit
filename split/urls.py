from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('groups/', views.GroupView.as_view(), name='group_view'),
    path('groups/view', views.GroupView.as_view(), name='group_views'),
    path('groups/new', views.GroupCreateView.as_view(), name='group_new'),
    path('groups/<int:pk>/', views.GroupDetailView.as_view(), name='group_detail'),
    path('groups/<int:pk>', views.group_view, name='group_view'),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.TemplateView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('cost/', views.CostView.as_view(), name='costs_list'),
    path('cost/new/', views.CostCreateView.as_view(), name='cost_new'),
    path('cost/<int:pk>/edit', views.CostEditView.as_view(), name='cost_edit'),
    path('cost/<int:pk>/delete', views.CostDeleteView.as_view(), name='cost_delete'),
    path('cost/<int:pk>/', views.CostDetailView.as_view(), name='cost_view'),
]