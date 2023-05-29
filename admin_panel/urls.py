from django.urls import path

from admin_panel import views

urlpatterns = [
    path('', views.adminHome, name='admin_home'),

    path('userCreate/',views.CreateUser,name='userCreation'),
    path('userEdit/user=<int:pk>/',views.EditUser,name='userEdit'),
    path('manageUsers/', views.ManageUser, name='manageUser'),
    path('userDelete/user=<int:pk>/',views.UserDelete,name='userDelete'),

    path('jobCreation/',views.JobCreation,name='jobCreation'),
    path('jobList/',views.JobList,name='jobList'),
    path('jobEdit/job=<int:job_id>',views.JobEdit,name='jobEdit'),
    path('jobDelete/job=<int:job_id>',views.JobDelete,name='jobDelete'),
    path("tagslist/", views.TagsList, name="tagslist"),

    path('jobApplications/', views.jobApplications, name='jobApplications'),
    path('jobApplicantslist/job=<int:job_id>', views.jobApplicants_list, name='jobApplicantlist'),
    path('jobApplicant_profile/applicant=<int:app_id>', views.jobApplicant_profile, name='jobApplicantProfile'),
    path('jobApplicant_Delete/applicant=<int:app_id>', views.JobApplicationDelete, name='jobApplicationDelete'),
    

    path('blogCreation/',views.BlogCreation,name='blogCreation'),
    path('blogList/',views.BlogList,name='blogList'),
    path('blogEdit/blog=<int:blog_id>/',views.BlogEdit,name='blogEdit'),
    path('blogDelete/blog=<int:blog_id>/',views.BlogDelete,name='blogDelete'),
    
    
    
]
