from django.shortcuts import render, redirect, get_object_or_404
from .forms import MenuItemForm, CategoryForm
from customer.models import MenuItem, Category

def menu_dashboard(request):
    form = MenuItemForm(request.POST or None, request.FILES or None)
    category_form = CategoryForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('deliver:menu_dashboard')

        if category_form.is_valid():
            category_form.save()
            return redirect('deliver:menu_dashboard')

    menu_items = MenuItem.objects.all()
    categories = Category.objects.all()
    context = {
        'form': form,
        'menu_items': menu_items,
        'category_form': category_form,
        'categories': categories
    }
    return render(request, 'deliver/menu_dashboard.html', context)


def menu_dashboardx(request):
    form = MenuItemForm(request.POST or None, request.FILES or None)
    category_form = CategoryForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('deliver:menu_dashboard')

        if category_form.is_valid():
            category_form.save()
            return redirect('deliver:menu_dashboard')

    menu_items = MenuItem.objects.all()
    categories = Category.objects.all()
    context = {
        'form': form,
        'menu_items': menu_items,
        'category_form': category_form,
        'categories': categories
    }
    return render(request, 'deliver/dashboardx.html', context)

def delete_item(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('deliver:menu_dashboard')

    return render(request, 'deliver/delete_item.html', {'item': item})


def update_item(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('deliver:menu_dashboard')
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'deliver/update_item.html', {'form': form, 'item': item})
