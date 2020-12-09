from django.urls import path, include
from . import views

app_name = "DeMatch"
urlpatterns = [
    path("", views.home, name="home"),    
    path('create_group', views.CreateGroupView, name='create_group')
]
