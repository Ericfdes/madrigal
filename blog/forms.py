from django.forms import ModelForm, Textarea
from blog.models import Comment, Blog
from dataclasses import field
from django import forms

# Create your forms here.

# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         widgets = {
#             'body': Textarea(attrs={'cols': 30, 'rows': 5}),
#         }

#         fields = '__all__'
#         exclude = ['user_pic','user_address','blog','commented_on']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['placeholder'] = field.help_text
            
class CommentForm(forms.ModelForm):
    # blog_id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
       model=Comment
       fields='__all__'
       exclude = ['user_address','commented_on','blog']
       
       widgets = {
             'user_name': forms.TextInput(attrs={"class": "form-control", "id":"basic-default-fullname"}),
             'user_email': forms.TextInput(attrs={"class": "form-control", "id":"basic-default-fullname"}),
             'body': forms.TextInput(attrs={"class": "form-control", "id":"basic-default-fullname"}),
        }
    # def __init__(self, *args, **kwargs):
    #     self.blog = kwargs.pop('blog')
    #     super().__init__(*args, **kwargs)
    #     self.fields['blog_id'].initial = self.blog.id

    # def save(self, commit=True):
    #     comment = super().save(commit=False)
    #     comment.blog = self.blog
    #     if commit:
    #         comment.save()
    #     return comment