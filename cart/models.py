# cart/models.py
from django.db import models
from django.conf import settings  # هذا مهم
from store.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # بدل auth.User
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
