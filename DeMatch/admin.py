from django.contrib import admin
from .models import User, Hobby, Subject, UserFriendRelation, Talk, Group, UserTalk, GroupTalk


admin.site.register(User)
admin.site.register(Hobby)
admin.site.register(Subject)
admin.site.register(UserFriendRelation)
admin.site.register(Group)
admin.site.register(GroupTalk)
admin.site.register(UserTalk)
