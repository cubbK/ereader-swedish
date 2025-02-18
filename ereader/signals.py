from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import EpubText
from .book_default_chunks import chunks


@receiver(post_save, sender=User)
def create_default_book(sender, instance, created, **kwargs):
    if created:
        EpubText.objects.create(
            user=instance,
            title="The young naval captain : The war of all nations by Edward Stratemeyer",
            text_chunks=chunks,
        )
