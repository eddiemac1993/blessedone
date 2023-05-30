from django import template

register = template.Library()

@register.filter
def convert_time(value):
    try:
        minutes = int(value)
        if minutes >= 60:
            hours = minutes // 60
            if hours >= 24:
                days = hours // 24
                if days >= 7:
                    weeks = days // 7
                    if weeks >= 4:
                        months = weeks // 4
                        return f"{months} month{'s' if months > 1 else ''} ago"
                    return f"{weeks} week{'s' if weeks > 1 else ''} ago"
                return f"{days} day{'s' if days > 1 else ''} ago"
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    except ValueError:
        return value
