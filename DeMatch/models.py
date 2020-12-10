from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Hobby(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.name


def check_email(value):
    if not "@st.kyoto-u.ac.jp" in value:
        raise ValidationError("ドメインが@st.kyoto-u.ac.jpのメールアドレスを使用してください。")


class User(AbstractUser):
    email = models.EmailField(validators=[check_email])
    belong_to = models.CharField(
        choices=[
            ("H", "総合人間学部"),
            ("L", "文学部"),
            ("P", "教育学部"),
            ("J", "法学部"),
            ("E", "経済学部"),
            ("S", "理学部"),
            ("Ma", "医学部｜医学科"),
            ("Mb", "医学部｜人間健康学科"),
            ("Ta", "工学部｜地球工学科"),
            ("Tb", "工学部｜建築学科"),
            ("Tc", "工学部｜物理工学科"),
            ("Td", "工学部｜電気電子工学科"),
            ("Te", "工学部｜工業化学科"),
            ("Tf", "工学部｜情報学科"),
            ("Aa", "農学部｜資源生物学科"),
            ("Ab", "農学部｜森林科学科"),
            ("Ac", "農学部｜食料・環境経済学科"),
            ("Ad", "農学部｜地域環境工学科"),
            ("Ae", "農学部｜応用生命科学科"),
            ("Af", "農学部｜食品生物学科"),
            ("Ph", "薬学部"),
        ],
        max_length=100,
        null=True,
        blank=True,
    )
    grade = models.CharField(
        choices=[
            ("B1", "学部１回生"),
            ("B2", "学部２回生"),
            ("B3", "学部３回生"),
            ("B4", "学部４回生"),
            ("M1", "修士１回生"),
            ("M2", "修士２回生"),
            ("D1", "博士１回生"),
            ("D2", "博士２回生"),
            ("D3", "博士３回生"),
            ("D4", "博士４回生"),
            ("D5", "博士５回生"),
        ],
        max_length=100,
        null=True,
        blank=True,
    )
    introduction = models.TextField(
        blank=True,
        null=True,
        max_length=200,
        default=None,
    )
    hobby = models.ManyToManyField("Hobby", related_name="hobby_user")
    subject = models.ManyToManyField("Subject", related_name="subject_user")
    friends = models.ManyToManyField(
        "self",
        symmetrical=False,
        through="UserFriendRelation",
        through_fields=("user", "friend"),
        related_name="friends_user",
    )
    requesting_friends = models.ManyToManyField(
        "self", symmetrical=False, related_name="being_requested_friends"
    )


class UserImg(models.Model):
    img = models.ImageField(upload_to="user_images")
    user = models.ForeignKey("User", on_delete=models.CASCADE)


class UserFriendRelation(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_relation")
    friend = models.ForeignKey("User", on_delete=models.CASCADE, related_name="friend_relation")
    is_blocked = models.BooleanField(default=False)


class Group(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(
        blank=True, null=True, verbose_name="group_image", upload_to="group_images"
    )
    hobby = models.ManyToManyField(Hobby, related_name="hobby_group")
    subject = models.ManyToManyField(Subject, related_name="subject_group")
    introduction = models.TextField(max_length=200, blank=True, null=True)
    member_list = models.ManyToManyField(User, related_name="group_member")
    inviting = models.ManyToManyField(User, related_name="inviting_user")
    applying = models.ManyToManyField(User, related_name="applying_user")

    def __str__(self):
        return self.name
