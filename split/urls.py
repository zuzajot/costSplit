from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.TemplateView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('cost/', views.CostListView.as_view(), name='costs_list'),
    path('cost/new/', views.CostCreateView.as_view(), name='cost_new'),
    path('cost/<int:pk>/edit', views.CostEditView.as_view(), name='cost_edit'),
    path('cost/<int:pk>/delete', views.CostDeleteView.as_view(), name='cost_delete'),
    path('cost/<int:pk>/', views.CostDetailView.as_view(), name='cost_view'),

    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/new', views.CreateGroupView.as_view(), name='group_create'),
    path('groups/<group_id>', views.group_view, name='group_view'),
    path('inv/<str:url>/', views.accept_or_decline_invitation, name='aod_invitation'), # aod = accept or decline
]
