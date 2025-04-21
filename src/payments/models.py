from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PayPalCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paypal_cards")
    payment_token = models.CharField(max_length=255)
    last4 = models.CharField(max_length=4)
    brand = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} ****{self.last4}"
