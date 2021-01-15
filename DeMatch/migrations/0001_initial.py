# Generated by Django 3.1.2 on 2020-12-29 13:55

import DeMatch.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserFriendRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_blocking', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, validators=[DeMatch.models.check_email])),
                ('main_img_source', models.ImageField(blank=True, null=True, upload_to='user_images')),
                ('sub1_img_source', models.ImageField(blank=True, null=True, upload_to='user_images')),
                ('sub2_img_source', models.ImageField(blank=True, null=True, upload_to='user_images')),
                ('sub3_img_source', models.ImageField(blank=True, null=True, upload_to='user_images')),
                ('belong_to', models.CharField(blank=True, choices=[('H', '総合人間学部'), ('L', '文学部'), ('P', '教育学部'), ('J', '法学部'), ('E', '経済学部'), ('S', '理学部'), ('Ma', '医学部｜医学科'), ('Mb', '医学部｜人間健康学科'), ('Ta', '工学部｜地球工学科'), ('Tb', '工学部｜建築学科'), ('Tc', '工学部｜物理工学科'), ('Td', '工学部｜電気電子工学科'), ('Te', '工学部｜工業化学科'), ('Tf', '工学部｜情報学科'), ('Aa', '農学部｜資源生物学科'), ('Ab', '農学部｜森林科学科'), ('Ac', '農学部｜食料・環境経済学科'), ('Ad', '農学部｜地域環境工学科'), ('Ae', '農学部｜応用生命科学科'), ('Af', '農学部｜食品生物学科'), ('Ph', '薬学部')], max_length=100, null=True)),
                ('grade', models.CharField(blank=True, choices=[('B1', '学部１回生'), ('B2', '学部２回生'), ('B3', '学部３回生'), ('B4', '学部４回生'), ('M1', '修士１回生'), ('M2', '修士２回生'), ('D1', '博士１回生'), ('D2', '博士２回生'), ('D3', '博士３回生'), ('D4', '博士４回生'), ('D5', '博士５回生')], max_length=100, null=True)),
                ('introduction', models.TextField(blank=True, default=None, max_length=200, null=True)),
                ('friend_requesting', models.ManyToManyField(blank=True, related_name='being_friend_requested', to=settings.AUTH_USER_MODEL)),
                ('friends', models.ManyToManyField(blank=True, through='DeMatch.UserFriendRelation', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('hobby', models.ManyToManyField(blank=True, related_name='hobby_user', to='DeMatch.Hobby')),
                ('subject', models.ManyToManyField(blank=True, related_name='subject_user', to='DeMatch.Subject')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='userfriendrelation',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userfriendrelation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, null=True, upload_to='group_images', verbose_name='group_image')),
                ('introduction', models.TextField(blank=True, max_length=200, null=True)),
                ('applying', models.ManyToManyField(related_name='applying_user', to=settings.AUTH_USER_MODEL)),
                ('hobby', models.ManyToManyField(related_name='hobby_group', to='DeMatch.Hobby')),
                ('inviting', models.ManyToManyField(related_name='inviting_user', to=settings.AUTH_USER_MODEL)),
                ('member_list', models.ManyToManyField(related_name='group_member', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ManyToManyField(related_name='subject_group', to='DeMatch.Subject')),
            ],
        ),
    ]
