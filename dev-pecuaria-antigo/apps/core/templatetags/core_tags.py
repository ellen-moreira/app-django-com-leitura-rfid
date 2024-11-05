from django import template
from django.contrib.auth.models import Group 

register = template.Library() 

@register.filter 
def is_pecuaria_member(user, group_name): 
    group = Group.objects.get(name='Pecuaria') 
    return group in user.groups.all()

@register.filter 
def is_edificios_member(user, group_name): 
    group = Group.objects.get(name='Edificios') 
    return group in user.groups.all() 