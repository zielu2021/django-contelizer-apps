import random
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages

def shuffle_word(word):
    if len(word) <= 3:
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
            
            new_filename = f"processed_{uploaded_file.name}"
            default_storage.save(new_filename, ContentFile(processed_content))

            messages.success(request, 'File uploaded and processed successfully!')
            return redirect('result', filename=new_filename)
        except UnicodeDecodeError:
            messages.error(request, 'Unable to read the file. Please ensure it contains valid text.')
            return render(request, 'file_handler/upload.html')
    
    return render(request, 'file_handler/upload.html')

def result(request, filename):
    try:
        with default_storage.open(filename, 'r') as file:
            processed_content = file.read()
        return render(request, 'file_handler/result.html', {'processed_content': processed_content})
    except FileNotFoundError:
        messages.error(request, 'The processed file was not found. Please try uploading again.')
        return redirect('upload_file')