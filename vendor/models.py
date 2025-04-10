# vendor/models.py
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.utils.text import slugify


from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


NOTIFICATION_TYPE = (
    ("New Order", "New Order"),
    ("New Review", "New Review"),
)

PAYOUT_METHOD = (
    ("PayPal", "PayPal"),
    ("Stripe", "Stripe"),    
    ("Nigerian Bank Account", "Nigerian Bank Account"),
    ("Indian Bank Account", "Indian Bank Account"),
    ("USA Bank Account", "USA Bank Account"),
)


TYPE = (
    ("New Order", "New Order"),
    ("Item Shipped", "Item Shipped"),
    ("Item Delivered", "Item Delivered"),
)



class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="vendor")
    image = models.ImageField(upload_to="vendor_images", default="shop-image.jpg", blank=True)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    vendor_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.store_name) if self.store_name else f"Vendor {self.vendor_id}"

    def save(self, *args, **kwargs):
        # Track if this is a new vendor
        is_new = self._state.adding
        
        # Generate slug if not exists
        if not self.slug and self.store_name:
            self.slug = slugify(self.store_name)
            
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Vendor.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # If approval status changed from False to True
        if not is_new:
            try:
                old_vendor = Vendor.objects.get(pk=self.pk)
                if not old_vendor.is_approved and self.is_approved:
                    self.send_approval_notification()
            except Vendor.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
    
    def send_approval_notification(self):
        """Send email notification when vendor is approved"""
        if self.user and self.user.email:
            subject = "Your Vendor Account Has Been Approved!"
            context = {
                'store_name': self.store_name,
                'login_url': f"{settings.SITE_URL}/auth/sign-in/",
                'dashboard_url': f"{settings.SITE_URL}/vendor/dashboard/",
            }
            
            # Render HTML email template
            html_message = render_to_string('email/vendor_approved.html', context)
            text_message = render_to_string('email/vendor_approved.txt', context)
            
            send_mail(
                subject,
                text_message,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                html_message=html_message,
                fail_silently=True,
            )



class Payout(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey("store.OrderItem", on_delete=models.SET_NULL, null=True, related_name="item")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payout_id = ShortUUIDField(unique=True, length=6, max_length=10, alphabet="1234567890")
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.vendor)
    
    class Meta:
        ordering = ['-date']

class BankAccount(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.SET_NULL, null=True)
    account_type = models.CharField(max_length=50, choices=PAYOUT_METHOD, null=True, blank=True, default="PayPal")
    
    bank_name = models.CharField(max_length=500)
    account_number = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=100, null=True, blank=True)

    stripe_id = models.CharField(max_length=100, null=True, blank=True)
    paypal_address = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Bank Account"

    def __str__(self):
        return self.bank_name


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="vendor_notifications")
    type = models.CharField(max_length=100, choices=TYPE, default=None)
    order = models.ForeignKey("store.OrderItem", on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Notification"
    
    def __str__(self):
        return self.type

