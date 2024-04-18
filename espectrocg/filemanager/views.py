import os
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
from django.conf import settings
from datetime import datetime

# Create your views here.
def index(request):
    # Get the list of all files and directories
    path = settings.MEDIA_ROOT
    dir_list = os.listdir(path + "/pdf")

    file = {"name": "", "size": "", "date": ""}
    list_of_files = []

    for file in dir_list:
        normal_date=datetime.fromtimestamp(os.path.getctime(path + "/pdf/" + file)).strftime('%Y-%m-%d %H:%M:%S')
        file = {"name": file, "size": os.path.getsize(path + "/pdf/" + file), "date": normal_date}
        list_of_files.append(file)

    return render(request, "main.html", { "files": list_of_files})


def about(request):
    return render(request, "about.html", {"name": "John Doe"})


# En tu archivo views.py
# @csrf_exempt
def subir_documento(request):
    if request.method == "POST":
        print(request.FILES)
        form = DocumentForm(request.POST, request.FILES)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = DocumentForm()
    return render(request, "upload_document.html", {"form": form})
