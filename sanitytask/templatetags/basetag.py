from django import template

from sanitytask.permission import get_user_permission_object

register = template.Library()


@register.simple_tag()
def task_tag(user):
    perm = get_user_permission_object(user)
    task_count = perm.get_task_count(user)
    return task_count


@register.simple_tag()
def lost_shift(user):
    perm = get_user_permission_object(user)
    if perm.get_alarm(user):
        return '!'
    else:
        return ''


@register.inclusion_tag('schedule_admin.html')
def schedule_admin(user):
    perm = get_user_permission_object(user)
    return {'perm': perm.has_perm()}


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
