import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EpubUploadForm
from .models import EpubText
import pypandoc
from django.http import HttpResponse
import tempfile
import os
from openai import OpenAI
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

client = OpenAI()


@login_required(login_url="/ereader/login/")
def index(request):
    books = EpubText.objects.filter(user=request.user).order_by("-uploaded_at")
    return render(request, "ereader/index.html", {"books": books})


@login_required(login_url="/ereader/login/")
def upload_epub(request):
    if request.method == "POST":
        form = EpubUploadForm(request.POST, request.FILES)
        if form.is_valid():
            epub_file = request.FILES["epub_file"]
            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in epub_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name

            # Path to the filter script
            filter_script = os.path.join(
                os.path.dirname(__file__), "./remove_images.py"
            )

            # Convert EPUB to text using pypandoc with the filter script
            output = pypandoc.convert_file(
                tmp_file_path,
                "plain",
                format="epub",
                extra_args=["--filter", filter_script],
            )

            def _chunk_book(output):
                chunks = []
                paragraphs = re.split(r"\n\s*\n", output)

                paragraphs = list(
                    map(
                        lambda p: re.sub(
                            r"\s+", " ", re.sub(r"--+", "", re.sub(r"\n", " ", p))
                        ).strip(),  # Remove dash sequences and newlines
                        paragraphs,
                    )
                )

                chunk_len = 0
                chunk = ""
                for paragraph in paragraphs:
                    chunk += paragraph + "\n"
                    chunk_len += len(paragraph)
                    if chunk_len > 2000:
                        chunks.append(chunk)
                        chunk = ""
                        chunk_len = 0
                return chunks

            chunks = _chunk_book(output)

            # Create EpubBook instance
            book = EpubText.objects.create(
                user=request.user, title=epub_file.name, text_chunks=chunks
            )

            return redirect("index")
    else:
        form = EpubUploadForm()
    return render(request, "ereader/upload_epub.html", {"form": form})


@login_required(login_url="/ereader/login/")
def reader(request, book_id, chunk_id):
    book = get_object_or_404(EpubText, id=book_id, user=request.user)
    if chunk_id < 0 or chunk_id >= len(book.text_chunks):
        return HttpResponse("Invalid chunk ID", status=400)
    original_chunk = book.text_chunks[chunk_id]

    previous_text = (
        book.text_chunks[chunk_id - 1][-len(book.text_chunks[chunk_id - 1]) // 4 :]
        if chunk_id > 0
        else ""
    )
    after_text = (
        book.text_chunks[chunk_id + 1][: len(book.text_chunks[chunk_id + 1]) // 4]
        if chunk_id < len(book.text_chunks) - 1
        else ""
    )

    promt = f"""
            I want to translate this part of a book text to swedish. Translate to EASY swedish. Make the sentence structure easy. Make the words easy. Simplify it to A1 level while maintaining the story meaning. output ONLY the translation. Use the previous text and after text to understand the context. previous text: "{previous_text}" after text: "{after_text}" text to translate: $BEGIN_TEXT${original_chunk}$END_TEXT$ " DO NOT SKIP ANY TEXT INSIDE $BEGIN_TEXT$ and $END_TEXT$
    """

    # Translate the chunk using OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": promt,
            }
        ],
        response_format={"type": "text"},
        temperature=1,
        max_completion_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    translated_chunk = response.choices[0].message.content

    # Save the last read chunk ID
    book.last_read_chunk = chunk_id
    book.save()

    return render(
        request,
        "ereader/reader.html",
        {
            "book": book,
            "original_chunk": original_chunk,
            "translated_chunk": translated_chunk,
            "chunk_id": chunk_id,
        },
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/ereader/")
    else:
        form = UserCreationForm()
    return render(request, "ereader/register.html", {"form": form})
