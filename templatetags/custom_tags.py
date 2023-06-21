from django import template

register = template.Library()

@register.simple_tag
def send_feedback():
    # Your tag implementation goes here
    return "Send feedback"
