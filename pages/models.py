from django.db import models


SUBJECT_CHOICES = [
    ("General Inquiry", "General Inquiry"),
    ("Support", "Support"),
    ("Feature Request", "Feature Request"),
    ("Advertising", "Advertising"),
]


class Contact(models.Model):
    name = models.CharField(default=None, blank=False, max_length=255)
    email = models.EmailField(max_length=255, default=None, blank=False)
    phone = models.CharField(max_length=18, default=None, null=True, blank=True)
    subject = models.CharField(
        max_length=50, choices=SUBJECT_CHOICES, default="General Inquiry"
    )
    message = models.TextField(default=None, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.email
