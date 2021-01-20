from django.conf import settings
from django.db import models


class Payment(models.Model):
    amount_paid = models.IntegerField()
    stripe_checkout_id = models.CharField(max_length=254)
    email = models.CharField(max_length=254)
    payment_status = models.CharField(max_length=50)
    purchase_type = models.CharField(max_length=50)
    purchase_choice = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="payments",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "payments"

    def __str__(self):
        return self.purchase_type + ': ' + self.purchase_choice

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
