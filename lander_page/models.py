from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12,default=None)
    message = models.TextField(max_length=500)
    contact_time = models.DateTimeField(db_comment="Date an time of contact")
