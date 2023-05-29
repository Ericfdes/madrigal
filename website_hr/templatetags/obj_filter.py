from django import template

register = template.Library() 

@register.filter(name='obj_filter') 
def obj_filter(Job, obj):
    return Job.filter(job=obj).count()

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
