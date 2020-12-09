from django import forms
from django.forms import ModelForm
from .models import User, Group

class CreateGroupForm(ModelForm):
  class Meta:
    model = Group
    fields = [
      'name',
      'image',
      'hobby',
      'subject',
      'introduction',
      'inviting',
    ]

  def __init__(self, user, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if user.friends():  
      self.fields['inviting'].queryset = User.objects.get(user=user).friends

  def create(self):
    name = self.cleaned_data['name']
    image = self.cleaned_data['image']
    hobby = self.cleaned_data['hobby']
    subject = self.cleaned_data['subject']
    introduction = self.cleaned_data['introduction']
    inviting = self.cleaned_data['inviting']
    group = Group(name=name, image=image, hobby=hobby, subject=subject, introduction=introduction, inviting=inviting)
    group.save()
