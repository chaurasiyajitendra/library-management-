from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=10,unique=True)
    password = models.CharField(max_length=16)

    def __str__(self):
        return self.username

class Book(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    description = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Rental(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="rentals")
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name="rentals")
    rented_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True,blank=True)
    returned = models.BooleanField(default=False)


    