from django.shortcuts import render
import os
from pathlib import Path
from .models import User, Hobby, Subject, UserFriendRelation, UserImg, Group
from .forms import (
    CreateGroupForm,
    InputProfileForm,
    MainImageForm,
    Sub1ImageForm,
    Sub2ImageForm,
    Sub3ImageForm,
)
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def home(request):
    user = request.user
    params = {
        "user": user,
    }
    return render(request, "DeMatch/home.html", params)


def input_profile(request):
    params = {"form": InputProfileForm()}
    return render(request, "DeMatch/input_profile.html", params)


def crop_center(img):
    img_width, img_height = img.size
    return img.crop(
        (
            (img_width - min(img.size)) // 2,
            (img_height - min(img.size)) // 2,
            (img_width + min(img.size)) // 2,
            (img_height + min(img.size)) // 2,
        )
    )


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
