from django import forms
from .models import JobApplication
from admin_panel.models import *
from blog.models import *
from ckeditor_uploader.fields import RichTextUploadingFormField

class JobCreationForm(forms.ModelForm):
    class Meta:
       model=Job
       fields='__all__'
       exclude = ('user', 'job_id', 'created_at')
       
       widgets = {
            'title': forms.TextInput(attrs={"class": "form-control", "id":"basic-default-fullname"}),
            'description': RichTextUploadingFormField(),
            'location': forms.TextInput(attrs={ "class": "form-control", "id":"basic-default-fullname"}),
            'type':forms.Select(attrs={ "class": "form-control", "id":"defaultSelect","for":"defaultSelect"}),
            'qualification':forms.TextInput(attrs={ "class": "form-control", "id":"basic-default-fullname"}),
            'experience':forms.TextInput(attrs={ "class": "form-control", "id":"basic-default-fullname"}),
            'last_date':forms.DateInput(attrs={ "class": "form-control","type":"date", "id":"html5-date-input","for":"defaultSelect"}),
            'company_name': forms.TextInput(attrs={"class": "form-control", "id":"basic-default-fullname"}),
            'company_description': forms.Textarea(attrs={"class": "form-control", "id":"basic-default-message","for":"basic-default-message" }),
            'tags':forms.SelectMultiple(attrs={"class": "form-control ui fluid search dropdown",  "multiple":""}),
            'vacancy': forms.NumberInput(attrs={"class": "form-control", "type":"number","id":"basic-default-message","for":"basic-default-message" }),
        }

    def __init__(self, *args, **kwargs):
        super(JobCreationForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].required = False   
        self.fields['company_description'].required = False   
       

class BlogCreationForm(forms.ModelForm):
    class Meta:
       model=Blog
       fields='__all__'
       exclude = ('slug', 'updated_on', 'created_on',)
       
       widgets = {
            'title': forms.TextInput(attrs={"class": "form-control", "id":"blog-title"}),
            'category':forms.Select(attrs={ "class": "form-control", "id":"blog-category","for":"blog-category"}),
            'blog_desc': forms.Textarea(attrs={"class": "form-control", "id":"basic-default-message","for":"basic-default-message" }),
            'author': forms.Select(attrs={ "class": "form-control", "id":"blog-author","for":"blog-author"}),
            'body': RichTextUploadingFormField(),
            'banner': forms.FileInput(attrs={"type": "file","class": "form-control", "id": "formFile", "accept": ".png, .jpg, .jpeg"}),
            'status':forms.Select(attrs={ "class": "form-control", "id":"blog-status","for":"blog-status"}),
        }   
       
class TagsForm(forms.ModelForm):
    class Meta:
       model=Tag
       fields='__all__'
  
       
       widgets = {
             'name': forms.TextInput(attrs={"class": "form-control", "id":"basic-default-fullname"})
        }





