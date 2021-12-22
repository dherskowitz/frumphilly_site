from django.db import models
from django.urls import reverse

SUBJECT_CHOICES = [
    ("", "Choose Subject"),
    ("Advertising", "Advertising"),
    ("Feature Request", "Feature Request"),
    ("General Inquiry", "General Inquiry"),
    ("Suggestion", "Suggestion"),
    ("Support", "Support"),
]


REPORT_REASON_CHOICES = [
    ("", "Choose Subject"),
    ("Content", "Inappropriate Content"),
    ("Images", "Inappropriate Images"),
    ("Quality", "Rude, Vulgar, or Offensive"),
    ("Ownership", "Copyright / Trademark Issue"),
    ("Spam", "Spam Content"),
]


class Contact(models.Model):
    STATUS_CHOICES = [
        ("unread", "Unread"),
        ("read", "Read"),
        ("spam", "Spam"),
    ]
    name = models.CharField(default=None, blank=False, max_length=255)
    email = models.EmailField(max_length=255, default=None, blank=False)
    phone = models.CharField(max_length=18, default=None, null=True, blank=True)
    subject = models.CharField(
        max_length=50, choices=SUBJECT_CHOICES, blank=False,
    )
    message = models.TextField(default=None, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, blank=False, null=False, default="unread"
    )

    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("contact_message", kwargs={"contact_id": self.id})


class ReportPost(models.Model):
    REPORT_STATUS_CHOICES = [
        ("reported", "Requires Review"),
        ("reviewing", "Under Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    post_type = models.CharField(default=None, blank=False, max_length=255)
    post_id = models.IntegerField(default=None, blank=False)
    post_title = models.CharField(default=None, blank=False, max_length=255)
    post_url = models.CharField(default=None, blank=False, max_length=255, null=True)
    status = models.CharField(
        max_length=50, choices=REPORT_STATUS_CHOICES, blank=False, null=True, default='reported'
    )
    report_reason = models.CharField(
        max_length=50, choices=REPORT_REASON_CHOICES, blank=False,
    )
    message = models.TextField(default=None, blank=True, null=True)
    user_id = models.IntegerField(default=None, blank=True, null=True)
    name = models.CharField(default=None, blank=True, max_length=255, null=True)
    email = models.EmailField(max_length=255, default=None, blank=True, null=True)
    form_email = models.EmailField(max_length=255, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reported Post"
        verbose_name_plural = "Reported Posts"

    def __str__(self):
        return f"Post {self.post_title} reported for {self.report_reason}"
