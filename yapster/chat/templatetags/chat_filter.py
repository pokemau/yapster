from django import template

register = template.Library()

@register.filter
def contains(value:str, substring:str):
    return value in substring 

@register.filter
def slice(value:str):
    return value.replace("[WORDLE]", "").strip()