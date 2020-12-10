from django.shortcuts import render
from .models import User, Hobby, Subject, UserFriendRelation, UserImg, Group
from .forms import CreateGroupForm, InputProfileForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    user = request.user
    friends = user.friends
    requesting_friends = user.requesting_friends
    being_requested_friends = user.being_requested_friends
    params = {
        "user": user,
        "friends": friends,
        "requesting_friends": requesting_friends,
        "being_requested_friends": being_requested_friends,
    }
    return render(request, "DeMatch/home.html", params)


def input_profile(request):
    params = {"form": InputProfileForm()}
    return render(request, "input_profile.html", params)
