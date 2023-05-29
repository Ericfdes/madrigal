from django import forms
from admin_panel.models import *
from authapp.models import *
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField


class JobApplyCVForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ("first_name", "last_name", "phone_number", "resume")
        labels = {
             'resume' : 'Upload CV',
            }

        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control", "id":"exampleFormControlInput1"}),
            'last_name': forms.TextInput(attrs={"class": "form-control", "id":"exampleFormControlInput1"}),
            'phone_number': PhoneNumberPrefixWidget(initial='IN'),
            'resume': forms.FileInput(attrs={"type": "file","class": "form-control", "id": "formFile", "accept": ".pdf, .docx, .txt" }),
        }

    def __init__(self, *args, **kwargs):
        
        self.user = kwargs.pop('user' , None)
        
        super(JobApplyCVForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        if self.user is not None:
            
            self.fields['first_name'].widget.attrs['value'] = self.user.first_name
            self.fields['last_name'].widget.attrs['value'] = self.user.last_name

        for field in self.fields.values():
            if isinstance(field, forms.CharField):
                field.widget.attrs['class'] = 'form-control'


class ApplyLinkedinForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "id":"exampleFormControlInput1"}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "id":"exampleFormControlInput1"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "id":"exampleFormControlInput1"}))
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))  
      

    def __init__(self, *args, **kwargs):
        
        self.user = kwargs.pop('user' , None)
        
        super(ApplyLinkedinForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field, forms.CharField):
                field.widget.attrs['class'] = 'form-control'


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id":"name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id":"email"}))
    subject = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id":"subject"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "id":"message"}))



class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("phone_number", "resume")
        labels = {
             'resume' : 'Upload CV',
            }

        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial='IN'),
            'resume': forms.FileInput(attrs={"type": "file","class": "form-control", "id": "formFile", "accept": ".pdf, .docx, .txt" }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.CharField):
                field.widget.attrs['class'] = 'form-control'


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.CharField):
                field.widget.attrs['class'] = 'form-control'
    
   
    


