from django.db import models

# Create your models here.
class Tracks(models.Model):
    title = models.CharField(max_length=255, null=False)
    artist = models.CharField(max_length=100, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)

    def __str__(self):
        return self.title

