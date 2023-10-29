from django.db import models
from accounts.models import Users
from PIL import Image

class Product(models.Model):
    name = models.CharField(max_length=99, verbose_name="نام محصول")
    image = models.ImageField(verbose_name="عکس محصول", null=True, blank=True)
    stock = models.PositiveIntegerField(verbose_name="موجودی محصول", default=0)
    price = models.PositiveBigIntegerField(verbose_name="قیمت محصول")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصول ها"

    def __str__(self):
        return self.name
        
class Order(models.Model):

    STATUS_CHOICES = (("1", "سبد خرید"),("2", "در حال پرداخت"),("3", "کنسل شده"),)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, verbose_name="کاربر")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
        
    @classmethod
    def get_basket(cls, user):
        basket = cls.objects.filter(user=user.id, status="1")
        if basket.exists():
            return basket.get()
        return None

    @classmethod
    def create_basket(cls, user):
        my_basket = cls(
            user=user,
            status=1
        )
        my_basket.save()
        return my_basket

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="سفارش")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="محصول")
    product_price = models.PositiveBigIntegerField(verbose_name="قیمت محصول")
    product_count = models.IntegerField(verbose_name="تعداد محصول")

    @classmethod
    def add(cls, order, product, count):
        prod = Product.objects.get(pk=product)
        data = cls.objects.filter(order=order, product__id=product)
        if data.exists():
            my_order_item = data.get()
            my_order_item.product_price = my_order_item.product.price
            my_order_item.product_count = my_order_item.product_count + 1
            my_order_item.save()
            return True
        else:
            instance = cls(order=order, product_price=prod.price,
                           product=prod, product_count=count)
            instance.save()
            return True

    @classmethod
    def remove(cls, order, product, count):
        data = cls.objects.filter(order=order, product__id=product)
        if data.exists():
            my_order_item = data.get()
            if my_order_item.product_count - count <= 0:
                target_order = my_order_item.order
                my_order_item.delete()
                return True
            else:

                my_order_item.product_count -= count
                my_order_item.save()
                return True
        else:
            return False

    class Meta:
        verbose_name = "ایتم"
        verbose_name_plural = "ایتم ها"
        