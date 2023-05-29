from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify
from django_resized import ResizedImageField
# Create your models here.


#Blog Models
STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE, default='')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey('Author', on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    body = RichTextUploadingField(blank=True, null=True)
    blog_desc = models.CharField(max_length=200, default = '')
    created_on = models.DateTimeField(auto_now_add=True)
    banner = ResizedImageField(size=[780, 438],upload_to="blog/blog_banners/", null=True, blank=True )
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(self.created_on))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title + " by " +str(self.author)

class Author(models.Model):
    author_name= models.CharField(max_length=100)
    author_desc= models.CharField(max_length=2000, null=True)
    author_prof= models.CharField(max_length=100, null=True)
    author_pic= models.ImageField(upload_to="blog/author_pic/", null=True, blank=True)
    #Socials
    twitter = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    stack_overflow = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.author_name

class Category(models.Model):
    category = models.CharField(max_length=50, default="Other")

    def __str__(self):
        return self.category

class Comment(models.Model):
    user_name= models.CharField(max_length=250, help_text='Name')
    user_email = models.EmailField(max_length=300, blank=True, help_text='E-mail')
    user_address=models.CharField(max_length=50, default='Unknown')
    body= models.TextField(max_length=4000, null=True, help_text='Comment')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='blog_comments', null=True)
    commented_on=models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-commented_on']

    def __str__(self):
        return self.user_name