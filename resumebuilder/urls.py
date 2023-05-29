from django.urls import path

from resumebuilder import views

urlpatterns = [
    path('', views.resume_builder, name='resume_builder'),
    path('generate_resume', views.generate_resume, name='generateResume')
    # path('view_resume/', views.view_resume, name='viewResume'),    
]
