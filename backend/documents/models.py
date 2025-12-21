from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to="documents/")
    doc_name = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
