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
        group = form.save()
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Groupの作成に失敗しました。")
        return super().form_invalid(form)

#groupの詳細
#id一致で取得。id情報はurlに組み込む
def GroupDetailView(request, pk):
    group = Group.objects.get(id=pk)
    #htmlの表示を切り替える変数をここで設定
    #他にいい方法がありそうなのであったら教えてください
    #condition 0はメンバー　1は招待中　2は申請中　3はどれでもない
    if group.member_list.filter(User=request.user):
        condition = 0
    elif group.inviting.filter(User=request.user):
        condition = 1
    elif group.applying.filter(User=request.user):
        condition = 2
    else:
        condition = 3
    params = {
        'group':group,
        'condition':condition
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

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Groupの作成に失敗しました。")
        return super().form_invalid(form)

  
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
