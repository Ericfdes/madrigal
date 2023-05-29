from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from admin_panel.models import *

from admin_panel.forms import *
from authapp.decorators import staff_only
from authapp.forms import RegisterForm, AdminUpdateUserForm
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.
@staff_only
def adminHome(request):
    messages.success(request, "Welcome to admin")
    return render(request, 'admin_home.html')


#User
@staff_only
def CreateUser(request):
    employee_group = Group.objects.get(name='employee')
    if request.method =='POST':
        userForm = RegisterForm(request.POST)
        if userForm.is_valid():
            employee = userForm.cleaned_data['employee']
            user = userForm.save()
            if employee == True:
                user.groups.add(employee_group)

            messages.success(request, "SUCCESS")
            print(user)
        else:
            for field, errors in userForm.errors.items():
                messages.error(request,'Field: {}, Errors: {}'.format(field, ','.join(errors)))
    else:
        userForm = RegisterForm()

    context = {
        'userCreateForm': userForm,
    }
    return render(request, 'CreateUser.html', context)

@staff_only
def ManageUser(request):
    userList = User.objects.all()

    context = {
        'userList': userList,
    }
    return render(request, 'ManageUser.html', context)

@staff_only
def EditUser(request, pk=None):

    employee_group = Group.objects.get(name='employee')
    user = get_object_or_404(User, id=pk)

    userForm = AdminUpdateUserForm(request.POST or None, instance=user)
    if request.method == 'POST':
            if userForm.is_valid():
                employee_status = request.POST.get('employee')
                print(f"Employement Status:{employee_status}")
                userForm.save()
                
                if employee_status == 'on':
                    user.groups.add(employee_group)
                else:
                    user.groups.remove(employee_group)

                messages.success(request, "User Edited Successfully!")
                # Save was successful, so redirect to another page
                redirect_url = reverse('manageUser')
                return redirect(redirect_url)
    context={
        'user':user,
        'userCreateForm': userForm,
    }
    
    return render(request,'EditUser.html',context )

@staff_only
def UserDelete(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    messages.success(request, "User Deleted Successfully!")
    return redirect('manageUser')



#Jobs
@staff_only
def JobCreation(request):

    if request.method == 'POST':
        jobCreateForm = JobCreationForm(request.POST)
        if jobCreateForm.is_valid():
            jobform =jobCreateForm.save(commit=False)
            jobform.user = request.user
            jobform.save()
            jobCreateForm.save_m2m()
            messages.success(request, "Success!")

        # else:
        #     print(jobCreateForm.errors)
        #     messages.error(request, "Error!")
    
    jobCreateForm = JobCreationForm()
    context={
        'jobCreateForm': jobCreateForm, 
    }
    
    return render(request,'JobCreation.html',context )


@staff_only
def JobList(request):
    jobList = Job.objects.all()
    context = {
        'jobList': jobList,
    }
    return render(request, 'JobList.html', context)


@staff_only
def JobEdit(request, job_id=None):

    
    job = get_object_or_404(Job, job_id=job_id)

    form = JobCreationForm(request.POST or None, instance=job)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, "Job Edited Successfully!")
        # Save was successful, so redirect to another page
        redirect_url = reverse('admin_home')
        return redirect(redirect_url)
    context={
        'jobCreateForm': form, 
    }
    
    return render(request,'JobEdit.html',context )

@staff_only
def JobDelete(request, job_id):
    job = Job.objects.get(job_id=job_id)
    job.delete()
    messages.success(request, "Job Deleted Successfully!")
    return redirect('jobList')

@staff_only
def jobApplications(request):
    jobApplications = JobApplication.objects.all()
    jobs = Job.objects.all()
    context = {
        'jobApplications' : jobApplications,
        'jobs': jobs,
    }
    return render(request, 'jobApplications.html', context)

@staff_only
def jobApplicants_list(request, job_id=None):
    jobApplications = JobApplication.objects.filter(job=job_id)
    
    context = {
        'jobApplications' : jobApplications,
        
    }
    return render(request, 'jobApplicants_list.html', context)

@staff_only
def jobApplicant_profile(request, app_id=None):
    jobApplication = get_object_or_404(JobApplication, application_id=app_id)
    if jobApplication.response == False:
        jobApplication.status='3'
        jobApplication.save()



    # Email For Accept
    acceptSubject = f'Job Offer: {jobApplication.job.title}'
    acceptText = f'Dear {jobApplication.first_name} {jobApplication.last_name}, \
                \n\nCongratulations! We are pleased to inform you that you have been accepted for the position of {jobApplication.job.title}.\
                Your application will now be forwarded to the company for further consideration.\
                \n\nWe appreciate your interest in the position and are impressed by your qualifications and experience.\
                \n\nPlease let us know if you have any questions or concerns.\n\nThank you for applying, and we wish you all the best in your new opportunity.\n\nBest regards,\nExecutive Recruiter\nAspire Corporate Solutions'
    
    rejectSubject = f"Subject: Regarding Your Job Application for {jobApplication.job.title}"
    rejectText = f"Dear {jobApplication.first_name} {jobApplication.last_name},\
                \n\nWe regret to inform you that we are unable to offer you the position of {jobApplication.job.title} at this time. We received many excellent applications, and the decision was a difficult one.\
                \n\nPlease be assured that your application was carefully reviewed and considered. We appreciate the time and effort you put into your application, and we thank you for your interest in working with us.\
                \n\nWe wish you all the best in your future job search and hope you will keep us in mind for future opportunities.\
                \n\nThank you for applying with us.\
                \n\nBest regards,\
                \n\nExecutive Recruiter\
                \nAspire Corporate Solutions"
   
    if request.method == 'POST':

        if 'acceptForm' in request.POST:
            accept_message = request.POST.get('acceptTextarea')
            send_mail(acceptSubject, accept_message, settings.EMAIL_HOST_USER,[jobApplication.email])
            
            jobApplication.status='5'
            jobApplication.response = True
            jobApplication.save()

            messages.success(request, "Response sent to applicant!")
        elif 'rejectForm' in request.POST:
            reject_message = request.POST.get('rejectTextarea')
            send_mail(rejectSubject, reject_message, settings.EMAIL_HOST_USER,[jobApplication.email])
            jobApplication.status='6'
            jobApplication.response= True
            jobApplication.save()
            messages.success(request, "Response sent to applicant!")
    
    context = {
        'applicant' : jobApplication,
        'accepttext': acceptText,
        'rejecttext': rejectText,
    }
    return render(request, 'applicant_profile.html', context)

@staff_only
def JobApplicationDelete(request, app_id):
    jobApplication = JobApplication.objects.get(pk=app_id)
    jobApplication.delete()
    messages.success(request, "Job Application Deleted Successfully!")
    return redirect('jobApplications')

#Blogs
@staff_only
def BlogCreation(request):

    if request.method == 'POST':
        blogCreateForm = BlogCreationForm(request.POST, request.FILES)
        if blogCreateForm.is_valid():
            blogCreateForm.save()
            messages.success(request, "Blog Created Successfully!")

        else:
            for field, errors in blogCreateForm.errors.items():
                messages.error(request,'Field: {}, Errors: {}'.format(field, ','.join(errors)))

    
    blogCreateForm = BlogCreationForm()
    context={
        'blogCreateForm': blogCreateForm, 
    }
    
    return render(request,'CreateBlog.html',context )

@staff_only
def BlogList(request):
    blogList = Blog.objects.all()
    context = {
        'blogList': blogList,
    }
    return render(request, 'ListBlog.html', context)

@staff_only
def BlogEdit(request, blog_id=None):

    
    blog = get_object_or_404(Blog, pk=blog_id)

    form = BlogCreationForm(request.POST or None, instance=blog)
    if request.POST and form.is_valid():
        form = BlogCreationForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog Edited Successfully!")
            # Save was successful, so redirect to another page
            redirect_url = reverse('admin_home')
            return redirect(redirect_url)
    context={
        'blogEditForm': form, 
    }
    
    return render(request,'EditBlog.html',context )

@staff_only
def BlogDelete(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    blog.delete()
    messages.success(request, "Blog Deleted Successfully!")
    return redirect('blogList')


@staff_only
def TagsList(request):

    tags = Tag.objects.all()
    # Group tags by the first letter of their name
 
    # Group tags by the first letter of their name
    tag_groups = []
    current_letter = None
    current_group = None
    for tag in tags:
        first_letter = tag.name[0].upper()
        if first_letter != current_letter:
            if current_group is not None:
                tag_groups.append((current_letter, current_group))
            current_letter = first_letter
            current_group = []
        current_group.append(tag)
    if current_group is not None:
        tag_groups.append((current_letter, current_group))
    # Pass the tag groups to the template for rendering

 

    if request.method == 'POST':
        TagForm = TagsForm(request.POST)
        if TagForm.is_valid():
         
            TagForm.save()
            messages.success(request, "New Tag Added!")

        # else:
        #     print(jobCreateForm.errors)
        #     messages.error(request, "Error!")
    
    tagsform=TagsForm()

 
    context={
        'tagsform': tagsform, 
        'tag_groups': tag_groups
    }
    
    return render(request, 'taglist.html', context)