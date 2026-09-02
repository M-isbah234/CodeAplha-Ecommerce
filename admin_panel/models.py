from django.db import models

class StoreSettings(models.Model):
    # Store Details & Localization
    default_currency = models.CharField(max_length=10, default='PKR')
    timezone = models.CharField(max_length=50, default='Asia/Karachi')
    support_email = models.EmailField(default='support@apexmarket.com')
    support_phone = models.CharField(max_length=20, default='+92 300 1234567')
    
    # System Controls
    staff_roles_enabled = models.BooleanField(default=True, help_text="Enable different access levels for staff (e.g. Catalog Editor vs Superuser)")
    email_webhooks_enabled = models.BooleanField(default=True, help_text="Send automated email receipts via webhooks")
    auto_maintenance = models.BooleanField(default=False, help_text="Automatically run database maintenance scripts weekly")

    class Meta:
        verbose_name = 'Store Setting'
        verbose_name_plural = 'Store Settings'

    def __str__(self):
        return "Global Store Settings"

    def save(self, *args, **kwargs):
        self.pk = 1 # Singleton pattern
        super(StoreSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
