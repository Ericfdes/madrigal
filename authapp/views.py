from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import  Group, User
from django.contrib import messages


from django.contrib.auth.forms import *
from django.urls import reverse
from .models import *

from authapp.forms import *

from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site  
from django.utils import six  
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from django.db.models.query_utils import Q

from social_django.utils import load_backend, load_strategy, psa

from social_core.backends.linkedin import LinkedinOAuth2

 #import messages



def user_login(request):
    if request.method == 'POST':
        username=request.POST['email-username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user, backend='authapp.auth_backend_ep.EmailOrUsernameModelBackend')
                messages.success(request, "Logged in Successfully!")
                return redirect('home')
            else:
                 messages.error(request, "Account is not active!")
        else:
            messages.error(request, f"Invalid Credentials. Please try again...")
            return redirect('user_login')

    context = {
       
    }

    return render(request, 'login.html', context)



def user_register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        

        if(User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists()):
            messages.error(request, "User with E-mail or Username already Exists!")
        else:
            if(password2 == password):
                user = User.objects.create_user(
                                                first_name=first_name,
                                                last_name=last_name,
                                                username=username,
                                                email=email,
                                                password=password)
                profile = Profile(user=user)
                profile.save()
                userSocials = UserSocials(profile=profile)
                userSocials.save()
                user.is_active = False  
                user.save()
               
                current_site = get_current_site(request)
                
                #Email
                mail_subject = 'Activation link has been sent to your email id'  
                message = render_to_string('acc_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  
                })  
                email_from = settings.EMAIL_HOST_USER
                to_email = [email]
                send_mail(mail_subject, message , email_from ,to_email )

                messages.success(request, f"Email has been sent to {user.email}. please check your inbox to verify your account")
                return redirect('home')
    return render(request, 'register.html')

    

def activate(request, uidb64, token):  
    User = get_user_model()  
    group = Group.objects.get(name='employee')
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.groups.add(group)
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')  
        return redirect('user_login')
    else:
        messages.error(request, 'Activation link is invalid!')    
        return redirect('home')


def user_logout(request):
    auth_logout(request)
    messages.info(request, "Logged out successfully!")

    return redirect('home')



def password_reset_request(request):
        
        if request.method == "POST":
                password_reset_form = UserPasswordResetForm(request.POST)
                if password_reset_form.is_valid():
                        data = password_reset_form.cleaned_data['email']
                        associated_users = User.objects.get(email=data)
                        print(associated_users)
                        if associated_users:
                                subject = "Password Reset Requested"
                                email_template_name = "password_reset_email.html"
                                c = {
                                "email":associated_users,
                                'domain':'127.0.0.1:8000',
                                'site_name': 'Website',
                                "uid": urlsafe_base64_encode(force_bytes(associated_users.pk)),
                                'token': default_token_generator.make_token(associated_users),
                                'protocol': 'http',
                                }
                                email_to_user = render_to_string(email_template_name, c)
                                try:
                                    send_mail(subject, email_to_user, settings.EMAIL_HOST_USER , [associated_users.email], fail_silently=False)
                                except BadHeaderError:

                                    return HttpResponse('Invalid header found.')
                                    
                                messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                                return redirect ("home")
                        else:
                             print("user not found")  
                        messages.error(request, 'An invalid email has been entered. :')
        password_reset_form = UserPasswordResetForm()
        return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})



def policy(request):
     return render(request, 'policy.html')


class TokenGenerator(PasswordResetTokenGenerator):  
        def _make_hash_value(self, user, timestamp):  
            return (  
                six.text_type(user.pk) + six.text_type(timestamp) +  
                six.text_type(user.is_active)  
            )  
account_activation_token = TokenGenerator()  



