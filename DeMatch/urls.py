from django.urls import path, include
from . import views

app_name = "DeMatch"
urlpatterns = [
    path("", views.home, name="home"),
    path("input_profile", views.input_profile, name="input_profile"),
]
