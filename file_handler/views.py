import random
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from django.http import HttpResponse

def shuffle_word(word):
    if len(word) < 4: 
        return word
    middle = list(word[1:-1])
    random.shuffle(middle)
    return word[0] + ''.join(middle) + word[-1]

def process_text(text):
    words = text.split()
    shuffled_words = [shuffle_word(word) for word in words]
    return ' '.join(shuffled_words)

def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, 'No file was uploaded. Please select a file before submitting.')
            return render(request, 'file_handler/upload.html')
        
        uploaded_file = request.FILES['file']
        if not uploaded_file.name.endswith('.txt'):
            messages.error(request, 'Invalid file type. Please upload a .txt file.')
            return render(request, 'file_handler/upload.html')
        
        try:
            file_content = uploaded_file.read().decode('utf-8')
            processed_content = process_text(file_content)
            
            messages.success(request, 'File processed successfully!')
            return render(request, 'file_handler/result.html', {'processed_content': processed_content, 'original_filename': uploaded_file.name})
        except UnicodeDecodeError:
            messages.error(request, 'Unable to read the file. Please ensure it contains valid text.')
            return render(request, 'file_handler/upload.html')
    
    return render(request, 'file_handler/upload.html')

def save_result(request):
    if request.method == 'POST':
        processed_content = request.POST.get('processed_content')
        original_filename = request.POST.get('original_filename')
        if processed_content and original_filename:
            new_filename = f"processed_{original_filename}"
            default_storage.save(new_filename, ContentFile(processed_content))
            response = HttpResponse(processed_content, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{new_filename}"'
            return response
    return redirect('upload_file')