from django.shortcuts import  render
from django.contrib import messages
from blog.forms import CommentForm
from .models import *

# Create your views here.

def blogs(request):
    blog_list = Blog.objects.all()
    context = {
        'nbar': 'blog',
        'blogs': blog_list,
    }
        

    return render(request, 'blog.html', context)

def blogDetails(request, slug_url):
    blog = Blog.objects.get(slug=slug_url)
    

    if request.method == 'POST':
        comment_form= CommentForm(request.POST)
        if comment_form.is_valid():
            
            obj = comment_form.save(commit=False)
            obj.blog= blog
            obj.save()
            messages.success(request, "Your comment has been posted successfully!")
            # return JsonResponse({'user_name':obj.user_name, 'commented_on':obj.commented_on, 'user_address':obj.user_address, 'body':obj.body})
            
   
    comment_form= CommentForm()
        

    # comment_form= CommentForm()

    context= {
        'comment_form' : comment_form,
        'blog': blog, 
        'nbar': 'blog',
    }

    return render(request, "blog-details.html", context)



# def blogDetails(request, slug_url):
#     blog = Blog.objects.filter(slug=slug_url).first()
    

#     if request.method == 'POST':
#         comment_form= CommentForm(request.POST)
#         if comment_form.is_valid():
            
#             comment_form.save()
          
#             messages.success(request, "Your comment has been posted successfully!")
#             # return JsonResponse({'user_name':obj.user_name, 'commented_on':obj.commented_on, 'user_address':obj.user_address, 'body':obj.body})
            
   
#     comment_form = CommentForm(blog=blog)
        

#     # comment_form= CommentForm()

#     context= {
#         'comment_form' : comment_form,
#         'blog': blog, 
#         'nbar': 'blog',
#     }

#     return render(request, "blog-details.html", context)