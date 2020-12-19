from django import forms
from .models import User, Group, Hobby, Subject


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            "name",
            "image",
            "hobby",
            "subject",
            "introduction",
            "inviting",
        ]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.friends():
            self.fields["inviting"].queryset = User.objects.get(user=user).friends

    def create(self):
        name = self.cleaned_data["name"]
        image = self.cleaned_data["image"]
        hobby = self.cleaned_data["hobby"]
        subject = self.cleaned_data["subject"]
        introduction = self.cleaned_data["introduction"]
        inviting = self.cleaned_data["inviting"]
        group = Group(
            name=name,
            image=image,
            hobby=hobby,
            subject=subject,
            introduction=introduction,
            inviting=inviting,
        )
        group.save()


class InputProfileForm(forms.ModelForm):
    hobby = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects, widget=forms.CheckboxSelectMultiple
    )
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            "username",
            "belong_to",
            "grade",
            "introduction",
            "hobby",
            "subject",
        ]


class MainImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "main_img_source",
        ]


class Sub1ImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "sub1_img_source",
        ]


class Sub2ImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "sub2_img_source",
        ]


class Sub3ImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "sub3_img_source",
        ]
