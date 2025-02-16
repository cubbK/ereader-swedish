from django.db import models
from django.contrib.auth.models import User

class EpubText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)