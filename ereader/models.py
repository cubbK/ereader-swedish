from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class EpubText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text_chunks = ArrayField(models.TextField(), blank=True, default=list)
    uploaded_at = models.DateTimeField(auto_now_add=True)