from django.db import models

# Create your models here.
class Book(models.Model):
    price=models.CharField(max_length=100)
    title=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.price}-{self.title}"