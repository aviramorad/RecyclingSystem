from django.contrib import admin
from .models import website_products


# Register your models here.
# admin.site.register(website_products)
class ProductAdmin(admin.ModelAdmin):
  list_display = ("product_name", "Product_type", "value", "bin_type",)

admin.site.register(website_products, ProductAdmin)