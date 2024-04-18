from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DocumentForm


# Create your views here.
def index(request):
    return render(request, "main.html", {"name": "John Doe"})


def about(request):
    return render(request, "about.html", {"name": "John Doe"})


# En tu archivo views.py
def subir_documento(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = DocumentForm()
    return render(request, "upload_document.html", {"form": form})
