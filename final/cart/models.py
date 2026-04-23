from django.db import models
from django.contrib.auth.models import User
from shop.models import Card
from django.utils import timezone

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.card.name}"
    
# record of a purchase for order history
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=7, decimal_places=2)
    purchased_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} bought {self.quantity}x {self.card.name}"