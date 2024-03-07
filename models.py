from django.db import models

# Create your models here.
class website_products(models.Model):
  product_name = models.CharField(max_length=255)
  Product_type = models.BooleanField(default=False)
  value = models.PositiveIntegerField()
  bin_type = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.product_name}, {self.bin_type}"

