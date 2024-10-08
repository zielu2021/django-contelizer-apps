from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from bs4 import BeautifulSoup

class FileHandlerTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_upload_file_view(self):
        # Test GET request
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'file_handler/upload.html')

        # Test POST request with valid file
        test_content = 'This is a test file with some longer words like encyclopedia.'
        with open('test_file.txt', 'w') as f:
            f.write(test_content)
        
        with open('test_file.txt', 'rb') as f:
            response = self.client.post(reverse('upload_file'), {'file': f})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'file_handler/result.html')
        
        # Extract the processed content from the HTML response
        soup = BeautifulSoup(response.content, 'html.parser')
        processed_content = soup.find('div', class_='result-text').text.strip()
        
        print(f"Original content: {test_content}")
        print(f"Processed content: {processed_content}")
        
        # Check that the processed content contains shuffled words
        shuffled_words = processed_content.split()
        original_words = test_content.split()
        
        print(f"Original words: {original_words}")
        print(f"Shuffled words: {shuffled_words}")
        
        # Check that all original words are present (possibly shuffled)
        for word in original_words:
            if len(word) > 3:
                self.assertTrue(any(w.lower().startswith(word[0].lower()) and w.lower().endswith(word[-1].lower()) for w in shuffled_words),
                                f"Word '{word}' not found in processed content")
            else:
                self.assertTrue(any(w.lower() == word.lower() for w in shuffled_words),
                                f"Short word '{word}' not found in processed content")
        
        # Check that at least one word is shuffled
        self.assertTrue(any(word.lower() != original.lower() for word, original in zip(shuffled_words, original_words) if len(original) > 3),
                        "No words appear to be shuffled")
        
        # Check that the first and last letters of each word are preserved
        for word, original in zip(shuffled_words, original_words):
            if len(original) > 3:  # Only check words longer than 3 letters
                self.assertEqual(word[0].lower(), original[0].lower(), 
                                 f"First letter not preserved: {word} (original: {original})")
                self.assertEqual(word[-1].lower(), original[-1].lower(), 
                                 f"Last letter not preserved: {word} (original: {original})")

        # Test POST request with no file
        response = self.client.post(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No file was uploaded')

        # Test POST request with invalid file type
        with open('test_file.jpg', 'w') as f:
            f.write('This is not a text file.')
        
        with open('test_file.jpg', 'rb') as f:
            response = self.client.post(reverse('upload_file'), {'file': f})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid file type')

    def test_process_text(self):
        from .views import process_text
        
        input_text = "This is a test sentence."
        processed = process_text(input_text)
        
        self.assertEqual(processed[0], 'T')
        self.assertEqual(processed[3], 's')
        self.assertEqual(processed[5], 'i')
        self.assertEqual(processed[6], 's')
        
        self.assertEqual(len(processed.split()), len(input_text.split()))

    def test_save_result(self):
        processed_content = "This is a prcosesd txet."
        original_filename = "original.txt"
        
        response = self.client.post(reverse('save_result'), {
            'processed_content': processed_content,
            'original_filename': original_filename
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="processed_original.txt"')
        self.assertEqual(response.content.decode(), processed_content)

    def tearDown(self):
        import os
        if os.path.exists('test_file.txt'):
            os.remove('test_file.txt')
        if os.path.exists('test_file.jpg'):
            os.remove('test_file.jpg')