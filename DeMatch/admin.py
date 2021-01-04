from django.contrib import admin
from .models import User, Hobby, Subject, UserFriendRelation, Talk, Group


admin.site.register(User)
admin.site.register(Hobby)
admin.site.register(Subject)
admin.site.register(UserFriendRelation)
admin.site.register(Talk)
admin.site.register(Group)
