from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EpubUploadForm
from .models import EpubText
import pypandoc
from django.http import HttpResponse
import tempfile
import os


@login_required
def index(request):
    books = EpubText.objects.filter(user=request.user)
    return render(request, 'ereader/index.html', {'books': books})

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
            
            # Split the output into chunks of around 2000 characters
            chunk_size = 2000
            def chunk_generator(text, size):
                for i in range(0, len(text), size):
                    yield text[i:i + size]

            chunks = list(chunk_generator(output, chunk_size))
            
            # Ensure chunks are split by word
            for i in range(len(chunks) - 1):
                if not chunks[i].endswith(' '):
                    last_space = chunks[i].rfind(' ')
                    if last_space != -1:
                        chunks[i + 1] = chunks[i][last_space + 1:] + chunks[i + 1]
                        chunks[i] = chunks[i][:last_space + 1]
            
            # Create EpubBook instance
            book = EpubText.objects.create(user=request.user, title=epub_file.name, text_chunks=chunks)
        
            
            return redirect('index')
    else:
        form = EpubUploadForm()
    return render(request, 'ereader/upload_epub.html', {'form': form})

@login_required
def reader(request, book_id, chunk_id):
    book = get_object_or_404(EpubText, id=book_id, user=request.user)
    if chunk_id < 0 or chunk_id >= len(book.text_chunks):
        return HttpResponse("Invalid chunk ID", status=400)
    original_chunk = book.text_chunks[chunk_id]
    translated_chunk = book.text_chunks_translated[chunk_id] if chunk_id < len(book.text_chunks_translated) else ""
    
    # Save the last read chunk ID
    book.last_read_chunk = chunk_id
    book.save()
    
    return render(request, 'ereader/reader.html', {'book': book, 'original_chunk': original_chunk, 'translated_chunk': translated_chunk, 'chunk_id': chunk_id})
