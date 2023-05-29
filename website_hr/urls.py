from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('404/', views.errorpage, name='404'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),

    path('jobs/', views.jobs, name='jobs'),
    path('jobDetail/', views.jobDetail, name='jobDetails'),
    path('jobDetail/job_id=<int:job_id>/', views.jobDetail, name='jobDetails'),
    path('jobDetail2/', views.jobDetail2, name='jobDetails2'),

    path('applied-jobs/', views.appliedJobs, name='appliedJobs'),
    path('trackJob/jobapplication_id=<int:jobapplication_id>/', views.trackJob, name='trackJob'),
    path('service1/',views.service1,name='service1'),
    path('service2/',views.service2,name='service2'),
    path('service3/',views.service3,name='service3'),
    path('service4/',views.service4,name='service4'),
    path('service5/',views.service5,name='service5'),
    path('profile/',views.profile,name='profile'),
    path('editProfile/user_id=<int:user_id>',views.profileEdit,name='profileEdit'),
]