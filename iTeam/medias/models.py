
from django.db import models

class Facebook(models.Model):
    access_token = models.CharField(max_length=256)
    expires = models.DateTimeField()
