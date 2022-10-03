from django.urls import path
from group import views

app_name = 'group'

urlpatterns = [
    path('', views.AllGroup.as_view(), name="all_group"),
    path("create/", views.CreateGroup.as_view(), name="create_group"),
    path("create/success", views.CreateGroupSuccess.as_view(), name="create_group_success"),
    path("<slug>/", views.GroupDetail.as_view(), name="group_detail"),
    path("<slug>/join/", views.JoinGroup.as_view(), name="join"),
    path("<slug>/leave/", views.LeaveGroup.as_view(), name="leave"),
    path("<slug>/delete/", views.DeleteGroup.as_view(), name="delete"),
]
