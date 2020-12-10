from django.urls import path, include
from . import views

app_name = "DeMatch"
urlpatterns = [
    path("", views.home, name="home"),    
    path("create_group/", views.GroupCreateView.as_view(), name="create_group"),
    path("group_detail/<int:pk>/", views.GroupDetailView, name="group_detail"),
]
