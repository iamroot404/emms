from django.db import models
from accounts.models import Account
import uuid

from django.db.models.deletion import CASCADE

# Create your models here.
class Meal(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to='meals', default="meals/default.png")
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.meal_name

    class Meta:
        ordering = ['-created_at']


class Menu(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    date = models.DateTimeField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.date

    class Meta:
        ordering = ['-created_at']
    

class BookingRequest(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    class Meta:
        ordering = ['-created_at']


class Bookings(models.Model):
    owner = models.ForeignKey(BookingRequest, on_delete=models.CASCADE, null=True)
    approved_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    class Meta:
        ordering = ['-created_at']




    
