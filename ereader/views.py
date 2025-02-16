from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EpubUploadForm
from .models import EpubText
import pypandoc
from django.http import HttpResponse
import tempfile
import os


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def upload_epub(request):
    if request.method == 'POST':
        form = EpubUploadForm(request.POST, request.FILES)
        if form.is_valid():
            epub_file = request.FILES['epub_file']
            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in epub_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name

            # Path to the filter script
            filter_script = os.path.join(os.path.dirname(__file__), './remove_images.py')

            # Convert EPUB to text using pypandoc with the filter script
            output = pypandoc.convert_file(tmp_file_path, 'plain', format='epub', extra_args=['--filter', filter_script])
            EpubText.objects.create(user=request.user, title=epub_file.name, text=output)
            return redirect('index')
    else:
        form = EpubUploadForm()
    return render(request, 'ereader/upload_epub.html', {'form': form})
# Create your views here.
