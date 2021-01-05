from django.urls import path, include
from . import views


app_name = "DeMatch"
urlpatterns = [
    # ホーム画面
    path("", views.Home.as_view(), name="home"),
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
    path("block/<int:pk>/", views.block, name="block"),
    # 自分の詳細（編集ページへのリンク付き）
    path("user_detail/", views.UserDetail.as_view(), name="user_detail"),
    # ブロックリスト
    path("block_list/", views.BlockList.as_view(), name="block_list"),
    #グループ作成ぺージ
    path("create_group/", views.GroupCreateView.as_view(), name="create_group"),
    #グループ詳細ページ
    path("group_detail/<int:pk>/", views.GroupDetailView, name="group_detail"),
    #グループ更新ページ
    path("group_update/<int:pk>/", views.GroupUpdateView.as_view(), name="group_update"),
    #検索ページ
    path("account_search/", views.account_search, name="account_search"),
    path("group_search/", views.group_search, name="group_search"),
    #検索結果ページ
    path("account_search_result/", views.account_search_result, name="account_search_result"),
    path("group_search_reusult/", views.group_search_result, name="group_search_result"),
    #おすすめ
    path("recommended/", views.recommended, name="recommended"),
    #ユーザーとのトークルーム
    path('DeMatch/User/<int:pk>/', views.room, name='room'),
    #グループとのトークルーム
    path('DeMatch/Group/<int:pk>/', views.group_room, name='group_room'),
    path('talk_list/', views.user_talk_list, name="user_talk_list"),
    path("group_list/", views.group_talk_list, name="group_talk_list"),
]
