from django.http import BadHeaderError, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from admin_panel.models import *
from django.contrib import messages
from website_hr.forms import *
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from authapp.models import Profile
from blog.models import *
from website_hr.forms import UpdateUserForm
# Create your views here.

def index(request):
    blog = Blog.objects.all().order_by("-created_on")[:4]
    context = {
        'blog': blog, 
        'nbar': 'home'
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'nbar': 'about'
    }
    return render(request, 'about.html', context)

def contact(request):
    if request.method == 'POST':
        print("Post form")
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
            'name': form.cleaned_data['name'],
            'subject': form.cleaned_data['subject'],
            'email': form.cleaned_data['email'],
            'message': form.cleaned_data['message'],
            }
            
            email_header = "A new client is trying to contact you:"
            # message = "\n".join([email_header] + [f"{key}: {value}" for key, value in body.items()])
            # response = "Your message has been sent. Thank you!"

            #Email to User
            subject = "Received Inquiry"
            message = f"Hi {body.get('name')}, we have received your email. We'll get back to you shortly."
            email = body.get('email')

            #Email to Comapny
            subject_company = f"(Website Inquiry) "+body.get('subject')
            message_company = "\n".join([email_header] + [f"Name:\n{body.get('name')} \n\nMessage: \n{body.get('message')}"])
            

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER,[email])

                #Email to Company
                send_mail(subject_company, message_company, email,[settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            # return redirect('contact')
        else:
            print(form.errors)
      
    form = ContactForm()
    context = {
        'form':form,
        'nbar': 'contact',
    }
    return render(request, "contact.html", context)


def services(request):
    services = Services.objects.all()
    context = {
        'services' : services,
        'nbar': 'services',
    }
    return render(request, 'services.html', context)

def jobs(request):
    search_post = request.GET.get('search')
    if search_post:
        keywords = search_post.split()
        query = Q()
        for keyword in keywords:
            query |= Q(title__icontains=keyword)  | Q(location__icontains=keyword) | Q(tags__name__icontains=keyword)
        jobs = Job.objects.filter(query).distinct()
    else:
        jobs = Job.objects.all().order_by("-created_at")
    
    context = {
        search_post:'search_post',
        'jobs': jobs,
        'nbar': 'jobs'
    }
    return render(request, 'jobs.html', context)

def jobDetail(request, job_id=None):
    job_detail = get_object_or_404(Job, job_id=job_id)
    request.session['job_url'] = job_id

    if request.method == 'POST':
        
        if 'applyJobCv' in request.POST:
            jobApplyForm= JobApplyCVForm(request.POST, request.FILES)
            if jobApplyForm.is_valid():
                jobApplyForm_cv=jobApplyForm.save(commit=False)
                if request.user.is_authenticated:
                    jobApplyForm_cv.user = request.user
                jobApplyForm_cv.email = request.POST.get('cv-email')
                jobApplyForm_cv.job = job_detail
                jobApplyForm_cv.provider = request.POST.get('applyProviderCV')
                
                jobApplyForm_cv.save()

                messages.success(request, "Applied for Job Successfully!")
            else:
                for field, errors in jobApplyForm.errors.items():
                    messages.error(request,'Field: {}, Errors: {}'.format(field, ','.join(errors)))
                print(jobApplyForm.errors)


        elif "applyJobLink" in request.POST:
            jobApplyLinkForm = ApplyLinkedinForm(request.POST)  
            if jobApplyLinkForm.is_valid():
                if request.user.is_authenticated:
                   job_application = JobApplication(
                            user = request.user,
                            job = job_detail,
                            email = jobApplyLinkForm.cleaned_data['email'],
                            first_name = jobApplyLinkForm.cleaned_data['first_name'],
                            last_name = jobApplyLinkForm.cleaned_data['last_name'],
                            phone_number = jobApplyLinkForm.cleaned_data['phone'],
                            provider = request.POST.get('applyProviderLink'))
                   job_application.save()
                else:
                    job_application = JobApplication(
                            job = job_detail,
                            email = jobApplyLinkForm.cleaned_data['email'],
                            first_name = jobApplyLinkForm.cleaned_data['first_name'],
                            last_name = jobApplyLinkForm.cleaned_data['last_name'],
                            phone_number = jobApplyLinkForm.cleaned_data['phone'],
                            provider = request.POST.get('applyProviderLink'))
                    job_application.save()

                del request.session['apply_linkedin_form']
                del request.session['job_url']
                messages.success(request, "Applied for Job Successfully!")
            else:
                 for field, errors in jobApplyLinkForm.errors.items():
                    messages.error(request,'Field: {}, Errors: {}'.format(field, ','.join(errors)))

    
    if request.user.is_authenticated:
        jobApplyForm = JobApplyCVForm(user=request.user)
    else:
        jobApplyForm = JobApplyCVForm(user=None)


    if 'apply_linkedin_form' in request.session:
        jobApplyLinkForm = ApplyLinkedinForm(initial=request.session.get('apply_linkedin_form', None))

    else:
        jobApplyLinkForm = ApplyLinkedinForm()
    
    context = {
        'nbar': 'jobs',
        'job': job_detail,
        'jobApplyForm': jobApplyForm,
        'jobApplyLinkForm': jobApplyLinkForm, 
    }
    return render(request, 'jobDetails.html', context)




def jobDetail2(request, job_id=None):
    job = get_object_or_404(Job, job_id=job_id)
    print(job)

    context = {
        'job': job,
    }
    return render(request, 'jobDetails2.html', context)

@login_required
def appliedJobs(request):
    jobs = JobApplication.objects.filter(user = request.user)
    applied_jobs = []
    for job in jobs:
        applied_jobs.append(job)

    print(applied_jobs)
    context = {
        'nbar': 'Profile',
        'jobs': applied_jobs,
    }

    return render(request, 'applied_joblist.html', context)

@login_required
def trackJob(request, jobapplication_id=None):
    job = get_object_or_404(JobApplication, application_id=jobapplication_id)
    print(job)

    context = {
        'nbar': 'Profile',
        'job': job,
    }
    return render(request, 'trackJob.html', context)

def service1(request):
    context = {
        'nbar': "services",
    }
    return render(request,'service1.html', context)

def service2(request):
    context = {
        'nbar': "services",
    }
    return render(request,'service2.html', context)

def service3(request):
    context = {
        'nbar': "services",
    }
    return render(request,'service3.html', context)

def service4(request):
    context = {
        'nbar': "services",
    }
    return render(request,'service4.html', context)

def service5(request):
    context = {
        'nbar': "services",
    }
    return render(request,'service5.html', context)

@login_required
def profile(request):
    if request.user.is_authenticated:

        user = get_object_or_404(Profile, user=request.user)
        userSocials = get_object_or_404(UserSocials, profile=user)
        context = {
            'nbar': 'Profile',
            'user':user,
            'socials': userSocials, 
        }
        return render(request, 'profile.html', context)
    else:
        HttpResponse("Not Authenthicated!")

@login_required
def profileEdit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, user=user)

    userForm = UpdateUserForm(request.POST or None, instance=user)
    profileform = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        profileform = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if all([userForm.is_valid() , profileform.is_valid()]):
            userForm.save()
            profileform.save()
            messages.success(request, "Changes saved successfully!")
            return redirect('profile')
        else:
            print("not Valid")

    context = {
        'nbar': 'Profile',
        'profile':profile,
        'user':user,
        'userForm': userForm,
        'profileForm': profileform,
    }
    return render(request, 'profile_edit.html', context)


def errorpage(request):
    return render(request, '404.html')


