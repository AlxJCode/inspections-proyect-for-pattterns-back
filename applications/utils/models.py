"""Django models utilities"""

# django
from django.db import models


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta option"""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']
