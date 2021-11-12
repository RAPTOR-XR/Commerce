from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass

class AuctionList(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="auction_user")
    title = models.CharField(max_length=80)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=80)
    starting_bid = models.FloatField(validators= [MinValueValidator(1)])
    active_status = models.BooleanField(blank=False, default=True)
    auction_winner = models.ForeignKey(User, on_delete=models.CASCADE ,blank=True, related_name="new_auction_user", null=True)

    def __str__(self):
        return (f"{self.title} -- {self.description} \t Starting Bid = {self.starting_bid}")

class AuctionBid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lists = models.ForeignKey(AuctionList, on_delete=models.CASCADE, verbose_name="Auction_price")
    input_value = models.FloatField(validators=[MinValueValidator(1)])
    auction_winner = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.user} has made a bid of {self.input_value} for the {self.lists} item.")

class AuctionComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lists = models.ForeignKey(AuctionList, on_delete=models.CASCADE)
    comment = models.TextField()

class AuctionWatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lists = models.ForeignKey(AuctionList, on_delete=models.CASCADE)