# En tu archivo forms.py

from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['filename', 'file']
        widgets = {
            'filename': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'filename': {
                'required': "El nombre de archivo es obligatorio.",
            },
        }
