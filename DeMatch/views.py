from django.shortcuts import render

from .models import User, Group
from .forms import CreateGroupForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

#groupの作成
class GroupCreateView(LoginRequiredMixin, generic.CreateView):
  model = Group
  template_name = 'create_group.html'
  from_class = CreateGroupForm
  success_url = reverse_lazy()


  
