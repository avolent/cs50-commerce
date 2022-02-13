from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f"ID:{self.id} - {self.username} | {self.email}"

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()
    image = models.TextField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    status = models.CharField(max_length=7, default="Open")
    def __str__(self):
        return f"{self.id}: {self.title}, Price: ${self.price}, Category: {self.category}, Seller:  {self.seller}, Status: {self.status}"

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddings")
    bid = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}: {self.auction.title}, Bid Amount: ${self.bid}, Bidder: {self.bidder.username}"

class Watchlist(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="followers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    def __str__(self):
        return f"User {self.user.username} has watchlisted {self.auction.title}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomments")
    comment = models.CharField(max_length=200, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}, {self.time} Commented: {self.comment}"
    