# Generated by Django 3.1.2 on 2021-01-02 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DeMatch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='テキスト')),
                ('time', models.DateTimeField(null=True)),
                ('talk_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_from', to=settings.AUTH_USER_MODEL)),
                ('talk_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]