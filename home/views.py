from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.views.decorators.clickjacking import xframe_options_exempt
import os

# Create your views here.
def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].lower()

@xframe_options_exempt
def home(request):
    context = {}
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

        file_extension = get_file_extension(name)
        
        context['url'] = url
        context['name'] = uploaded_file.name
        context['extension'] = file_extension
    return render(request, 'index.html', context)