from datetime import datetime
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    def __str__(self):
        return f"ID:{self.id} - {self.username} | {self.email}"

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_price = models.FloatField()
    image = models.TextField()
    category = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="sales")

    def __str__(self):
        return f"{self.id}: {self.title}, Starting price: {self.starting_price}, Category: {self.category}, Seller:  {self.seller}"