import markdown

from django import template
from django.utils.safestring import mark_safe

from iTeam.member.models import Profile

register = template.Library()

@register.filter
def iteam_markdown(value):
    html = markdown.markdown(value, safe_mode='escape', extensions=['codehilite(linenums=True)', 'extra'])
    return mark_safe(html)

@register.filter
def profile(user):
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    return profile

