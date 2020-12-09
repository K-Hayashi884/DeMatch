from django.shortcuts import render
from .models import User, Hobby, Subject, UserFriendRelation, UserImg, Group
from .forms import CreateGroupForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

#groupの作成
class GroupCreateView(LoginRequiredMixin, generic.CreateView):
  model = Group
  template_name = 'create_group.html'
  from_class = CreateGroupForm
  success_url = reverse_lazy()

  
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
