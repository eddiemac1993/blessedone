from django.db.models import Sum

def calculate_summaries(queryset):
    summaries = {
        'SC': queryset.filter(company='SC').aggregate(Sum('amount'))['amount__sum'] or 0,
        'CMM': queryset.filter(company='CMM').aggregate(Sum('amount'))['amount__sum'] or 0,
    }
    summaries['Total'] = summaries['SC'] + summaries['CMM']
    return summaries