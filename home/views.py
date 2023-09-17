from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(request):
    context = {}
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        context['url'] = url
        context['name'] = uploaded_file.name
    return render(request, 'index.html', context)