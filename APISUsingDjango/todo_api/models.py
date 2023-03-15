from django.db import models

# Create your models here.
class TodoApi(models.Model):
    todo = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.todo

