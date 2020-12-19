from django.urls import path, include
from . import views


app_name = "DeMatch"
urlpatterns = [
    # ホーム画面
    path("", views.home, name="home"),
    # 初回のプロフィール入力
    path("input_profile/", views.input_profile, name="input_profile"),
    # 通常のプロフィール編集
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    # 画像投稿ページ（↑から飛ぶ）
    path("cropping/<img_name>/", views.cropping, name="cropping"),
    # 他のユーザーの詳細
    path("friend_detail/<int:pk>/", views.FriendDetail.as_view(), name="friend_detail"),
    # 友達申請用のview関数
    path("friend_request/<int:pk>/", views.friend_request, name="friend_request"),
    # ブロック用のview関数
    path("block/<int:pk>/", views.block, name="block")
    # 自分の詳細（編集ページへのリンク付き）
    # path("user_detail/", views.UserDetail.as_view(), name="user_detail"),
]
