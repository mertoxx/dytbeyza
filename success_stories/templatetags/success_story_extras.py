# success_stories/templatetags/__init__.py
# Bu dosya tamamen boş olmalı

# success_stories/templatetags/success_story_extras.py
from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """İki sayıyı çıkar"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter  
def multiply(value, arg):
    """İki sayıyı çarp"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """İki sayıyı böl"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """Yüzdelik hesapla"""
    try:
        if float(total) == 0:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, TypeError):
        return 0