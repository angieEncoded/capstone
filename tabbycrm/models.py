from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related

# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=64)
    title = models.CharField(max_length=64, null=True, blank=True)
    department = models.CharField(max_length=64, null=True, blank=True)
    extension = models.CharField(max_length=64, null=True, blank=True)
    cellphone = models.CharField(max_length=64, null=True, blank=True)
    street = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=64, null=True, blank=True)
    zip = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    pass

# class Auction(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=64)
#     description = models.TextField()
#     starting_bid = models.FloatField(null=True)
#     url = models.CharField(blank=True, null=True, max_length=254)
#     high_bid = models.ForeignKey(
#         "Bid", on_delete=models.SET_NULL, related_name="current_high_bid", null=True, blank=True)
#     category = models.CharField(max_length=100)
#     listed_by = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="user_auctions")
#     winner = models.ForeignKey(
#         User, on_delete=models.SET_NULL, related_name="auction_winner", null=True, blank=True)
#     ended = models.BooleanField(default=False)


#     def __str__(this):
#         return f"id: {this.id} title: {this.title} description: {this.description} starting_bid:{this.starting_bid} url:{this.url} high_bid: {this.high_bid} category{this.category} listed_by: {this.listed_by} winner: {this.winner} ended:{this.ended}"


# class Bid(models.Model):
#     id = models.AutoField(primary_key=True)
#     bid_amount = models.FloatField()
#     bidder = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="bidder_name")
#     # related name lets us access things in the opposite
#     item_id = models.IntegerField()

#     def __str__(this):
#         return f"High Bid: {this.bid_amount} bidder: {this.bidder} item_id: {this.item_id}"


# class Comment(models.Model):
#     id = models.AutoField(primary_key=True)
#     item_id = models.ForeignKey(
#         Auction, on_delete=models.CASCADE, related_name="item_comments")
#     content = models.TextField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(this):
#         return f"id: {this.id} |  item_id: {this.item_id}  | content: {this.content} | user: {this.user}"


# class Category(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=64)
#     image = models.CharField(max_length=255, null=True, blank=True)

#     def __str__(this):
#         return f"{this.name}"


# class Watchlist(models.Model):
#     id = models.AutoField(primary_key=True)
#     item = models.ForeignKey(
#         Auction, on_delete=models.CASCADE, related_name="item_watching")
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="user_watching")