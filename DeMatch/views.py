from django.shortcuts import render
from .models import User, Hobby, Subject, UserFriendRelation, UserImg, Group
from .forms import CreateGroupForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

#groupの作成
class GroupCreateView(LoginRequiredMixin, generic.CreateView):
    model = Group
    template_name = 'group_create.html'
    from_class = CreateGroupForm
    success_url = reverse_lazy('group_detail')

    def form_valid(self, form):
      diary = form.save()
      return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Groupの作成に失敗しました。")

#groupの詳細
#id一致で取得。id情報はurlに組み込む
def GroupDetailView(request, pk):
    group = Group.objects.get(id=pk)
    params = {
        'group':group,
    }
    return render(request, "DeMatch/group_detail.html", params)

#groupの編集
#id一致で取得。id情報はurlに組み込む
class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Group
    template_name = 'group_update.html'
    form_class = CreateGroupForm
    
    def get_success_url(self):
        return reverse_lazy('group_detail', kwargs={'pk': self.kwargs['pk']})
    
    def form_invalid(self, form):
        messages.error(self.request, "Groupの作成に失敗しました。")

  
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
