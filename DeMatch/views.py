from django.shortcuts import render, redirect
from .models import User, Hobby, Subject, UserFriendRelation, Group, Talk, UserTalk, GroupTalk
from .forms import (
    CreateGroupForm,
    InputProfileForm,
    FindForm,
    GroupFindForm,
    GroupInviteForm,
)
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Q, Subquery
import datetime  
from django.http import HttpResponseRedirect

#groupの作成
class GroupCreateView(LoginRequiredMixin, generic.CreateView):
    model = Group
    template_name = "DeMatch/group_create.html"
    form_class = CreateGroupForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        print(self.request.user)
        return kwargs

    def get_success_url(self):
        return reverse('DeMatch:group_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        group = form.save()
        group.member_list.add(self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Groupの作成に失敗しました。")
        return super().form_invalid(form)



# groupの詳細
# id一致で取得。id情報はurlに組み込む
@login_required
def GroupDetailView(request, pk):
    group = Group.objects.get(pk=pk)
    user = request.user
    member_list = group.member_list
    inviting = group.inviting
    applying = group.applying
    if request.method == "GET":
    # htmlの表示を切り替える変数をここで設定
    # 他にいい方法がありそうなのであったら教えてください
    # condition 0はメンバー　1は招待中　2は申請中　3はどれでもない
        if member_list.filter(id=request.user.id):
            condition = 0
        elif inviting.filter(id=request.user.id):
            condition = 1
        elif applying.filter(id=request.user.id):
            condition = 2
        else:
            condition = 3
        params = {"group": group, "condition": condition}
    if request.method == "POST":
        if 'button_0' in request.POST:
            return HttpResponseRedirect(
        reverse('DeMatch:group_update', kwargs={"pk": pk}))
        elif 'button_5' in request.POST:
            return HttpResponseRedirect(
        reverse('DeMatch:group_invite', kwargs={"pk": pk}))
        elif 'button_1' in request.POST:
            condition = 0
            inviting.remove(user)
            member_list.add(user)
        elif 'button_2' in request.POST:
            condition = 3
        elif 'button_3' in request.POST:
            condition = 3
            applying.remove(user)
        elif 'button_4' in request.POST:
            condition = 2
            applying.add(user)
        elif 'button_6' in request.POST:
            member_list.remove(user)
            if member_list:
                group.delete()
        return HttpResponseRedirect(
        reverse(Home))
        params = {"group": group, "condition": condition}
    return render(request, "DeMatch/group_detail.html", params)

@login_required
def GroupInviteView(request, pk):
    user = request.user
    group = Group.objects.get(pk=pk)
    member_list = group.member_list
    inviting = group.inviting
    applying = group.applying
    friends = user.friends.exclude(group_member=group).exclude(inviting_user=group).exclude(applying_user=group)
    form = GroupInviteForm()
    if request.method == "GET":
        form.fields['invite'].queryset = friends
        #招待できる友達がいる：condition=0
        #いない：condition=1
        if friends:
            condition = 0
        else:
            condition = 1
        params = {
            'form':form,
            'pk':pk,
            'condition':condition,
        }
        return render(request, "DeMatch/group_invite.html", params)
    if request.method == "POST":
        print(request.POST.getlist("invite"))
        for friend in request.POST.getlist("invite"):
            group.inviting.add(friend)
            print(friend)
        return HttpResponseRedirect(
        reverse('DeMatch:group_detail', kwargs={"pk": pk}))

# groupの編集
# id一致で取得。id情報はurlに組み込む
class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Group
    template_name = "DeMatch/group_update.html"
    fields = ['name', 'image', 'hobby', 'subject', 'introduction']

    def get_success_url(self):
        return reverse_lazy("DeMatch:group_detail", kwargs={"pk": self.kwargs["pk"]})



# ホーム画面
class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = "DeMatch/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        being_requested_list = user.being_friend_requested.order_by("username")
        friend_list = user.friends.filter(friend_relation__is_blocking=False).order_by("username")
        requesting_list = user.friend_requesting.order_by("username")
        being_invited_list = user.inviting_user.order_by("name")
        requesting_group_list = user.applying_user.order_by("name")
        group_list = user.group_member.order_by("name")
        context["being_requested_list"] = being_requested_list
        context["friend_list"] = friend_list
        context["requesting_list"] = requesting_list
        context["being_invited_list"] = being_invited_list
        context["requesting_group_list"] = requesting_group_list
        context["group_list"] = group_list
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



@login_required
def account_search(request):
    form = FindForm()
    #hobbyとsubjectの選択肢をDBから取得して追加
    hobby_choices = Hobby.objects.all()
    #subject_choices = [(i.naem, i.name) for i in Subject.objects.all()]
    subject_choices = Subject.objects.all()

    form.fields["hobby"].queryset = hobby_choices
    form.fields["subject"].queryset = subject_choices
    params = {
        "form" : form,
    }

    if (request.method == 'POST'):
        form = FindForm(request.POST)
        keyword = request.POST['keyword']
        grade = request.POST.getlist('grade')
        belong_to = request.POST.getlist('belong_to')
        hobby = request.POST.getlist('hobby')
        subject  = request.POST.getlist('subject')
        choice_method = request.POST['choice_method']
        if (form.is_valid):
            if (choice_method == "or"):
                data = User.objects.filter(Q(username__icontains = keyword),Q(grade__in = grade)|
                              Q(belong_to__in = belong_to)|Q(hobby__in = hobby)|Q(subject__in = subject)).distinct().order_by('last_login').reverse()
            elif (choice_method == "and"):
                data = User.objects.filter(username__icontains = keyword).distinct().order_by('last_login').reverse()
                for i in grade:
                    data = data.filter(grade = i)
                for i in belong_to:
                    data = data.filter(belong_to = i)
                for i in hobby:
                    data = data.filter(hobby = i)
                for i in subject:
                    data = data.filter(subject = i)
            params = {
              'form' : FindForm(request.POST),
              'data' : data,
              'group_search' : 'group_search',
            }


        return render(request, "DeMatch/account_search_result.html", params)
        
    return render(request, "DeMatch/account_search.html", params) 


@login_required
def group_search(request):
    form = GroupFindForm()
    #hobbyとsubjectの選択肢をDBから取得して追加
    hobby_choices = Hobby.objects.all()
    subject_choices = Subject.objects.all()

    form.fields["hobby"].queryset = hobby_choices
    form.fields["subject"].queryset = subject_choices
    params = {
        "form" : form,
    }

    if (request.method == 'POST'):
        form = GroupFindForm(request.POST)
        keyword = request.POST['keyword']
        hobby = request.POST.getlist('hobby')
        subject  = request.POST.getlist('subject')
        choice_method = request.POST['choice_method']
        if (form.is_valid):
            if (choice_method == "or"):
                latest_msg = GroupTalk.objects.filter(
                    talk_from=OuterRef("pk") 
                ).order_by('time')
                data = Group.objects.filter(Q(name__icontains = keyword),
                                            Q(hobby__in = hobby)|Q(subject__in = subject)).distinct().annotate(
                    latest_msg_id=Subquery(
                        latest_msg.values("pk")[:1]
                    ),
                    latest_msg_content=Subquery(
                        latest_msg.values("text")[:1]
                    ), #これはなしでもいい
                    latest_msg_pub_date=Subquery(
                        latest_msg.values("time")[:1]
                    ), #これはなしでもいい
                ).order_by("-latest_msg_id")
                #メッセージ最終受信時間で並び替え
            elif (choice_method == "and"):
                latest_msg = GroupTalk.objects.filter(
                    talk_from=OuterRef("pk") 
                ).order_by('-time')
                data = Group.objects.filter(name__icontains = keyword).distinct().annotate(
                    latest_msg_id=Subquery(
                        latest_msg.values("pk")[:1]
                    ),
                    latest_msg_content=Subquery(
                        latest_msg.values("text")[:1]
                    ), #これはなしでもいい
                    latest_msg_pub_date=Subquery(
                        latest_msg.values("time")[:1]
                    ), #これはなしでもいい
                ).order_by("-latest_msg_id")
                
                for i in hobby:
                    data = data.filter(hobby = i)
                for i in subject:
                    data = data.filter(subject = i)
            params = {
              'form' : GroupFindForm(request.POST),
              'data' : data,
              'account_search' : 'account_search',
            }
        return render(request, "DeMatch/group_search_result.html", params)

    return render(request, "DeMatch/group_search.html", params) 


@login_required
def account_search_result(request):
    return render(request, "DeMatch/account_search_result.html")

@login_required
def group_search_result(request):
    return render(request, "DeMatch/group_search_result.html")


#おすすめ
@login_required
def recommended(request):
    user = request.user
    user_query = User.objects.filter(username = user.username)
    latest_msg = GroupTalk.objects.filter(
                    talk_from=OuterRef("pk") 
                  ).order_by('-time')
    data = Group.objects.filter(Q(hobby__in = user_query.values('hobby'))|
                    Q(subject__in = user_query.values('subject'))).distinct().annotate(
                    latest_msg_id=Subquery(
                        latest_msg.values("pk")[:1]
                    ),
                    latest_msg_content=Subquery(
                        latest_msg.values("text")[:1]
                    ), #これはなしでもいい
                    latest_msg_pub_date=Subquery(
                        latest_msg.values("time")[:1]
                    ), #これはなしでもいい
                  ).order_by("-latest_msg_id")
    params = {
      'data' : data,
    }
    return render(request, "DeMatch/recommended.html", params)

#チャットルームの表示
@login_required
def room(request, pk):
    user = request.user
    friend = User.objects.get(pk=pk)
    # 送信form
    log = UserTalk.objects.filter(Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend))
    params = {
        'username': user.username,
        'log':  log,
        'room_name': pk,
    }
    return render(request, 'DeMatch/chatroom.html', params)

#グループチャットルームの表示
@login_required
def group_room(request, pk):
    user = request.user
    group = Group.objects.get(pk=pk)
    # 送信form
    log = GroupTalk.objects.filter(talk_to=group)
    params = {
        'groupname': group.name,
        'log':  log,
        'room_name': pk,
    }
    return render(request, 'DeMatch/group_chatroom.html', params)

@login_required
def user_talk_list(request):
    user = request.user
   # ユーザーひとりずつの最新のトークを特定する
    latest_msg = UserTalk.objects.filter(
        Q(talk_from=OuterRef("pk"), talk_to=user) | Q(talk_from=user, talk_to=OuterRef("pk"))
    ).order_by('-time')
    friends = User.objects.exclude(id=user.id).annotate(
       latest_msg_id=Subquery(
           latest_msg.values("pk")[:1]
       ),
       latest_msg_content=Subquery(
           latest_msg.values("text")[:1]
       ),
       latest_msg_pub_date=Subquery(
           latest_msg.values("time")[:1]
       ),
    ).order_by("-latest_msg_id")
    params = {
        "user": user,
        "friends": friends,
    }
    return render(request, "DeMatch/user_talk_list.html", params)


@login_required
def group_talk_list(request):
    user = request.user
    latest_msg = GroupTalk.objects.filter(
      talk_to=OuterRef("pk")
    ).order_by('-time')
    groups = Group.objects.filter(member_list=user).annotate(
        latest_msg_id=Subquery(
            latest_msg.values("pk")[:1]
        ),
        latest_msg_content=Subquery(
            latest_msg.values("text")[:1]
        ),
        latest_msg_pub_date=Subquery(
            latest_msg.values("time")[:1]
        ),
    ).order_by("-latest_msg_id")
    params = {
        "user" : user,
        "groups" : groups,
    }
    return render(request, "DeMatch/group_talk_list.html", params)
