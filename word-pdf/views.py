from django.shortcuts import render, redirect
from .forms import UploadFileForm

# Create your views here.
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            # Handle the uploaded file (e.g., save it to a directory)
            # Redirect to a success page or perform additional processing
            return redirect('success')
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})
