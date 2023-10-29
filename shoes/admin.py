from django.contrib import admin
from shoes.models import Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "stock", "get_price"]
    search_fields = ["name", "stock"]

    def get_price(self, obj):
        return f"{obj.price} تومان"

    get_price.short_description = "قیمت محصول"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass