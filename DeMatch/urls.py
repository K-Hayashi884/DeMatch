from django.urls import path, include
from . import views

app_name = "DeMatch"
urlpatterns = [
  path('create_group', views.CreateGroupView, name='create_group')
]
