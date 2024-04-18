from django.db import models

# Create your models here.

class Document(models.Model):
    filename = models.CharField(max_length=100)
    file = models.FileField(upload_to='pdf/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
