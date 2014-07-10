from django import template
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

@register.filter
def iteam_markdown(value):
    html = markdown.markdown(value, safe_mode='escape')
    return mark_safe(html)
