# education/views.py

from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
import os
from django.conf import settings
from .models import PDFResource, BlogPost, SuccessStory
from .forms import FreeTrialForm

from django.http import HttpResponse

# views.py

from django.shortcuts import render
from django.http import HttpResponse
from pdf2image import convert_from_path
import os
from django.conf import settings

def view_pdf(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
    if os.path.exists(filepath):
        images = []
        # Convert PDF to images
        pages = convert_from_path(filepath, 300)  # adjust DPI as needed
        for i, page in enumerate(pages):
            image_path = f'media/pdf_images/{filename}_page_{i+1}.jpg'  # save images in media/pdf_images/
            page.save(os.path.join(settings.MEDIA_ROOT, 'pdf_images', f'{filename}_page_{i+1}.jpg'), 'JPEG')
            images.append(image_path)

        return render(request, 'education/pdf_view.html', {'images': images})
    else:
        return HttpResponse("PDF not found")



def index(request):
    pdf_resources = PDFResource.objects.all()
    blog_posts = BlogPost.objects.all()
    return render(request, 'education/index.html', {'pdf_resources': pdf_resources, 'blog_posts': blog_posts})

def free_trial(request):
    if request.method == 'POST':
        form = FreeTrialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FreeTrialForm()
    return render(request, 'education/free_trial.html', {'form': form})

def success_stories(request):
    success_stories = SuccessStory.objects.all()
    return render(request, 'education/success_stories.html', {'success_stories': success_stories})

def view_pdf(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    else:
        raise Http404
