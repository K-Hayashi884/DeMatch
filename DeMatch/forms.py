from django import forms
from .models import User, Group, Hobby, Subject
from django.forms.fields import ChoiceField


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = (
            "name",
            "image",
            "hobby",
            "subject",
            "introduction",
            "inviting",
        )
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     user = kwargs.pop('user')
    #     if user.friends:
    #         self.fields["inviting"].queryset = user.friends
    #     else:
    #         CHOICE_LIST = [
    #             ('', '----'),
    #         ]
    #         self.fields["inviting"].queryset =ChoiceField(choices=CHOICE_LIST, required=False)

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
            "main_img_source",
            "sub1_img_source",
            "sub2_img_source",
            "sub3_img_source",
        ]

#検索フォーム
class FindForm(forms.Form):
    keyword = forms.CharField(required=True, label='keyword') #検索キーワード
    grade = forms.MultipleChoiceField(label='grade', 
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
                ]) #学年
    belong_to = forms.ChoiceField(label='belong_to', 
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
                ]) #学部・学科
    hobby = forms.MultipleChoiceField(label='hobby', required=False) #趣味
    subject = forms.MultipleChoiceField(label='subjectField', required=False) #勉強分野
    choice_method = forms.ChoiceField(label='choiceMethod', 
        choices=[
            ('or', '部分一致'),
            ('and', '完全一致'),
                ]) #検索条件




#グループ検索フォーム
class GroupFindForm(forms.Form):
    keyword = forms.CharField(required=True, label='keyword') #検索キーワード
    
    hobby = forms.MultipleChoiceField(label='hobby', required=False) #趣味
    subject = forms.MultipleChoiceField(label='subjectField', required=False) #勉強分野
    choice_method = forms.ChoiceField(label='choiceMethod', 
        choices=[
            ('or', '部分一致'),
            ('and', '完全一致'),
                ]) #検索条件