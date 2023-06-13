from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import PDFUploadForm
from .models import PDFFile, Category

def pdf_upload(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_manager:pdf_list')
    else:
        form = PDFUploadForm()
    return render(request, 'pdf_manager/upload_pdf.html', {'form': form})



def pdf_list_view(request):
    query = request.GET.get('q')  # Get the search query from the URL parameters

    # Retrieve the list of categories
    categories = Category.objects.all()

    if query:
        pdf_files = PDFFile.objects.filter(
            Q(title__icontains=query) | Q(pdf__icontains=query)
        )
    else:
        pdf_files = PDFFile.objects.all()

    context = {
        'pdf_files': pdf_files,
        'query': query,
        'categories': categories,  # Add the categories to the context
    }

    return render(request, 'pdf_manager/pdf_list.html', context)