from django.shortcuts import render, redirect
from .models import User, Hobby, Subject, UserFriendRelation, UserImg, Group
from .forms import (
    CreateGroupForm,
    InputProfileForm,
    MainImageForm,
    Sub1ImageForm,
    Sub2ImageForm,
    Sub3ImageForm,
)
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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

#ホーム画面
class Home(generic.TemplateView, LoginRequiredMixin):
    template_name = "DeMatch/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        being_requested_list = user.being_friend_requested.order_by("username")
        friend_list = user.friends.order_by("username")
        requesting_list = user.friend_requesting.order_by("username")
        context["being_requested_list"] = being_requested_list
        context["friend_list"] = friend_list
        context["requesting_list"] = requesting_list
        return context


# 登録時のプロフィール入力
@login_required
def input_profile(request):
    form = InputProfileForm(instance=request.user)
    if request.method == "POST":
        form = InputProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    params = {"form": form}
    return render(request, "DeMatch/input_profile.html", params)


# 通常利用されるプロフィール編集
@login_required
def edit_profile(request):
    form = InputProfileForm(instance=request.user)
    if request.method == "POST":
        form = InputProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    params = {"form": form}
    return render(request, "DeMatch/edit_profile.html", params)


# アイコン画像投稿
@login_required
def cropping(request, img_name):
    msg = ""
    user = request.user
    if request.method == "POST":
        if img_name == "sub1":
            form = Sub1ImageForm(request.POST, request.FILES, instance=user)
        elif img_name == "sub2":
            form = Sub2ImageForm(request.POST, request.FILES, instance=user)
        elif img_name == "sub3":
            form = Sub3ImageForm(request.POST, request.FILES, instance=user)
        else:
            form = MainImageForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            msg = "画像を変更しました"
        else:
            msg = "画像の変更に失敗しました"

    if img_name == "sub1":
        title = "サブ画像１の設定"
        user_img = user.sub1_img
        form = Sub1ImageForm(instance=user)
    elif img_name == "sub2":
        title = "サブ画像２の設定"
        user_img = user.sub2_img
        form = Sub2ImageForm(instance=user)
    elif img_name == "sub3":
        title = "サブ画像３の設定"
        user_img = user.sub3_img
        form = Sub3ImageForm(instance=user)
    else:
        title = "メイン画像の設定"
        user_img = user.main_img
        form = MainImageForm(instance=user)
    params = {
        "form": form,
        "title": title,
        "user_img": user_img,
        "msg": msg,
    }
    return render(request, "DeMatch/cropping.html", params)


class FriendDetail(generic.DetailView, LoginRequiredMixin):
    template_name = "DeMatch/friend_detail.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend = context.get("object")
        user = self.request.user
        friend_flg = True if friend in user.friends.all() else False
        requesting_flg = True if friend in user.friend_requesting.all() else False
        being_requested_flg = True if friend in user.being_friend_requested.all() else False
        context["friend_flg"] = friend_flg
        context["requesting_flg"] = requesting_flg
        context["being_requested_flg"] = being_requested_flg
        if user.user_relation.filter(friend=friend).exists():
            blocking_flg = user.user_relation.get(friend=friend).is_blocking
        else:
            blocking_flg = False
        if friend.user_relation.filter(friend=user).exists():
            blocked_flg = friend.user_relation.get(friend=user).is_blocking
        else:
            blocked_flg = False
        context["blocking_flg"] = blocking_flg
        context["blocked_flg"] = blocked_flg
        return context


@login_required
def friend_request(request, pk):
    friend = User.objects.get(pk=pk)
    user = request.user
    friend_flg = True if friend in user.friends.all() else False
    requesting_flg = True if friend in user.friend_requesting.all() else False
    being_requested_flg = True if friend in user.being_friend_requested.all() else False
    if being_requested_flg:
        user.friends.add(friend)
        friend.friends.add(user)
        friend.friend_requesting.remove(user)
        UserFriendRelation.objects.create(user=user, friend=friend, is_blocking=False)
        UserFriendRelation.objects.create(user=friend, friend=user, is_blocking=False)
    elif requesting_flg:
        user.friend_requesting.remove(friend)
    else:
        user.friend_requesting.add(friend)
    return redirect(to=("../../friend_detail/" + str(pk)))


@login_required
def block(request, pk):
    friend = User.objects.get(pk=pk)
    user = request.user
    if UserFriendRelation.objects.filter(user=user, friend=friend).exists():
        blocking_flg = UserFriendRelation.objects.get(user=user, friend=friend).is_blocking
    else:
        blocking_flg = False
    if blocking_flg:
        UserFriendRelation.objects.get(user=user, friend=friend).delete()
    else:
        if UserFriendRelation.objects.filter(user=user, friend=friend).exists():
            user_friend_relation = UserFriendRelation.objects.get(user=user, friend=friend)
            user_friend_relation.is_blocking = True
            user_friend_relation.save()
        else:
            UserFriendRelation.objects.create(user=user, friend=friend, is_blocking=True)
    return redirect(to=("../../friend_detail/" + str(pk)))


class UserDetail(generic.TemplateView, LoginRequiredMixin):
    template_name = "DeMatch/user_detail.html"


class BlockList(generic.TemplateView, LoginRequiredMixin):
    template_name = "DeMatch/block_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        block_list = UserFriendRelation.objects.filter(user=user, is_blocking=True)
        context["block_list"] = block_list
        return context
