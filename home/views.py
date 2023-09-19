from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.clickjacking import xframe_options_exempt
import os
from pathlib import Path
import urllib.parse

BASE_DIR = Path(__file__).resolve().parent.parent

# from .main import is_ats_friendly

def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].lower()

@xframe_options_exempt
def home(request):
    context = {}
    global file_url
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

        file_extension = get_file_extension(name)
        
        request.session['url'] = url
        request.session['name'] = name

        context['url'] = url
        context['name'] = uploaded_file.name
        context['extension'] = file_extension
    return render(request, 'index.html', context)

import PyPDF2

def is_ats_friendly(url, name):
    print("THIS IS THE PDF URL:", url)
    url = url[1:]

    absolute_url = os.path.join(settings.MEDIA_ROOT, name)

    print("THIS IS AFTER I JOIN: ", absolute_url)

    keyword = ['skills', 'education', 'certifications', 'experience', 'projects', 'awards', 'linkedin']
    missing = []

    pdf_reader = PyPDF2.PdfReader(absolute_url)
    rating = 0

    text_content = ""

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text_content += page.extract_text()

    text_content = text_content.lower()
    print(text_content)
    j=0

    for i in keyword:
        if i in text_content:
            rating += 1
        else:
            print("THIS IS MISSING: ", i)
            missing.append(i)
    
    return rating, missing

def analyzer(request):
    url = urllib.parse.unquote(request.session.get('url'))
    name = request.session.get('name')

    print('name:', name)
    
    result = is_ats_friendly(url, name)

    rating, missing = result

    context = {}

    context['url'] = request.session.get('url')
    context['rating'] = rating
    context['missing'] = missing
    
    return render(request, 'ats.html', context)