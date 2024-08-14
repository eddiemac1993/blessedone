from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template.loader import render_to_string
from .forms import ExpenseForm
from .models import Expense
from .utils import calculate_summaries
import pdfkit
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import json
from django.db.models import Q

def dashboard(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=365)
    expenses = Expense.objects.filter(date__range=[start_date, end_date])

    # Expense trends over time
    monthly_expenses = expenses.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    trend_data = [[m['month'].strftime("%Y-%m"), float(m['total'])] for m in monthly_expenses]

    # Expense distribution by category
    category_expenses = expenses.values('category').annotate(total=Sum('amount')).order_by('-total')
    category_data = [float(c['total']) for c in category_expenses]
    category_labels = [c['category'] for c in category_expenses]

    # Top spending categories
    top_categories = category_expenses[:5]

    # Recent expenses
    recent_expenses = Expense.objects.all().order_by('-date')[:5]

    # Calculate totals
    total_last_30_days = expenses.filter(date__gte=end_date - timedelta(days=30)).aggregate(Sum('amount'))['amount__sum'] or 0
    avg_daily_expense = total_last_30_days / 30
    total_all_time = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'trend_data': json.dumps(trend_data),
        'category_data': json.dumps(category_data),
        'category_labels': json.dumps(category_labels),
        'top_categories': top_categories,
        'recent_expenses': recent_expenses,
        'total_last_30_days': total_last_30_days,
        'avg_daily_expense': avg_daily_expense,
        'total_all_time': total_all_time,
    }
    return render(request, 'finances/dashboard.html', context)

def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')

    filter_type = request.GET.get('filter', 'all')
    company = request.GET.get('company', 'all')
    search_query = request.GET.get('search', '')

    today = timezone.now().date()

    if filter_type == 'daily':
        expenses = expenses.filter(date=today)
    elif filter_type == 'weekly':
        week_ago = today - timedelta(days=7)
        expenses = expenses.filter(date__gte=week_ago)
    elif filter_type == 'monthly':
        month_ago = today - timedelta(days=30)
        expenses = expenses.filter(date__gte=month_ago)

    if company != 'all':
        expenses = expenses.filter(company=company)

    if search_query:
        expenses = expenses.filter(
            Q(reason__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(company__icontains=search_query)
        )

    summaries = calculate_summaries(expenses)

    context = {
        'expenses': expenses,
        'summaries': summaries,
        'filter_type': filter_type,
        'company': company,
    }
    return render(request, 'finances/expense_list.html', context)

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'finances/add_expense.html', {'form': form})

def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'finances/edit_expense.html', {'form': form, 'expense': expense})

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'finances/delete_expense.html', {'expense': expense})

def generate_pdf_report(request):
    filter_type = request.GET.get('filter', 'all')
    company = request.GET.get('company', 'all')

    expenses = Expense.objects.all().order_by('-date')

    if filter_type == 'daily':
        expenses = expenses.filter(date=timezone.now().date())
    elif filter_type == 'weekly':
        week_ago = timezone.now().date() - timedelta(days=7)
        expenses = expenses.filter(date__gte=week_ago)
    elif filter_type == 'monthly':
        month_ago = timezone.now().date() - timedelta(days=30)
        expenses = expenses.filter(date__gte=month_ago)

    if company != 'all':
        expenses = expenses.filter(company=company)

    summaries = calculate_summaries(expenses)

    context = {
        'expenses': expenses,
        'summaries': summaries,
        'filter_type': filter_type,
        'company': company,
        'current_date': timezone.now().strftime("%B %d, %Y"),
    }

    html = render_to_string('finances/pdf_report.html', context)
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="expense_report_{filter_type}_{company}.pdf"'
    return response