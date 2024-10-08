from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile 


class FileHandlerTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_upload_file_view_get(self):
        response = self.client.get(reverse('file_handler:upload_file'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'file_handler/upload.html')

    def test_upload_file_view_post_valid(self):
        test_file = SimpleUploadedFile("test.txt", b"This is a test file.")
        response = self.client.post(reverse('file_handler:upload_file'), {'file': test_file})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'file_handler/result.html')

    def test_save_result_view(self):
        response = self.client.post(reverse('file_handler:save_result'), {
            'processed_content': 'Sample content',
            'original_filename': 'original.txt'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')