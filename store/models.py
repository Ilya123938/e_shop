from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_("Category Name")
    )
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = _("Categories")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/category/{self.slug}/"


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_("Product Name")
    )

    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Category")
    )

    photo = models.ImageField(upload_to='products/')

    description = models.TextField(
        verbose_name=_("Product Description")
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price")
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name=_("Available")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/product/{self.slug}/"


class Contact(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name")
    )

    email = models.EmailField(
        verbose_name=_("Email")
    )

    subject = models.CharField(
        max_length=200,
        verbose_name=_("Subject")
    )

    message = models.TextField(
        verbose_name=_("Message")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return self.name