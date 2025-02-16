from django import forms

class EpubUploadForm(forms.Form):
    epub_file = forms.FileField()