from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Confirmation Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=_('Enter the same password as before, for verification.'),
    )

    employee = forms.BooleanField()

    class Meta:
        model = User
        fields = ('username','first_name','last_name',  'email', 'password1', 'password2', 'is_active',  'employee', 'is_staff')
 
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control", "id":"exampleFormControlInput1", "placeholder":"Enter your username"}),
            'first_name': forms.TextInput(attrs={"class": "form-control", "id":"exampleFormControlInput1",  "placeholder":"Enter your First name"}),
            'last_name': forms.TextInput(attrs={"class": "form-control", "id":"exampleFormControlInput1",  "placeholder":"Enter your Last name"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "id":"exampleFormControlInput1", "placeholder":"Enter your Email"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].required = False   
        for field in self.fields.values():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'

def check_group(request):
    if request.user.groups.exists():
        return True
    else:
        return False

class AdminUpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].required = False   
        for field in self.fields.values():
            if isinstance(field, forms.CharField):
                field.widget.attrs['class'] = 'form-control'
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your E-Mail',
        'type': 'email',
        'name': 'email'
        }))
    

class UserPasswordResetFormConfirm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetFormConfirm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter new Password',
        'type': 'password',
        'name': 'password'
        }))
    
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm new Password',
        'type': 'password',
        'name': 'password2'
        }))
    

