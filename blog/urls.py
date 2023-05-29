from django.urls import path

from blog import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('blogDetail/<str:slug_url>', views.blogDetails, name='blogDetails'),
]
