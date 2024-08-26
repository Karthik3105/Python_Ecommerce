from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.contrib.auth.models import User
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from cloudinary.models import CloudinaryField

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_code = models.CharField(max_length=50, unique=True)
    category_description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_code

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    product_details = models.TextField()
    product_image = models.CloudinaryField(upload_to='products/')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    @property
    def category_code(self):
        return self.category.category_id  # Compute category_code dynamically


    def __str__(self):
        return self.product_name
