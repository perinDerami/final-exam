from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from accounts.models import Users
import os
from shoes.models import Order, Product, OrderItem
from rest_framework.authtoken.models import Token


class HomeView(View):
    def get(self, request):
        pro = Product.objects.all()
        count = 0
        if request.user.is_authenticated:
            basket = Order.get_basket(request.user)
            if basket:
                count = len(basket.orderitem_set.all())
        response = render(request, "main.html", {"products": pro, "count": count})
        if request.user.is_authenticated and not request.COOKIES.get("token", None):
            token, _ = Token.objects.get_or_create(user=request.user)
            response.set_cookie(key="token", value=token)
        return response

    def post(self, request):
        type = request.POST.get("type")
        if type == "reset":
            basket = Order.get_basket(request.user)
            order_items = basket.orderitem_set.all()
            order_items.delete()
            return render(request, "main.html", {"products": Product.objects.all(), "count": 0})
        if type == "add":
            id = request.POST.get("product-id")
            href = request.POST.get("href")
            my_order = Order.objects.filter(user__id=request.user.id, status="1")
            if request.user.is_authenticated:
                if my_order.exists():
                    my_order = my_order.get()
                    OrderItem.add(my_order, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                    if href == "main":
                        return render(request, "main.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                    else:
                        pr = 0
                        for item in order_items:
                            pr += item.product.price
                        return render(request, "cart.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": pr})
                else:
                    basket = Order.create_basket(request.user)
                    OrderItem.add(basket, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                    if href == "main":
                        return render(request, "main.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                    else:
                        pr = 0
                        for item in order_items:
                            pr += item.product.price
                        return render(request, "cart.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": pr})
        elif type == "remove":
            id = request.POST.get("product-id")
            href = request.POST.get("href")
            my_order = Order.objects.filter(user__id=request.user.id, status="1")
            if request.user.is_authenticated:
                if my_order.exists():
                    my_order = my_order.get()
                    OrderItem.remove(my_order, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                    if href == "main":
                        return render(request, "main.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                    else:
                        pr = 0
                        for item in order_items:
                            pr += item.product.price
                        return render(request, "cart.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": pr})
                else:
                    basket = Order.create_basket(request.user)
                    OrderItem.remove(basket, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                    if href == "main":
                        return render(request, "main.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                    else:
                        pr = 0
                        for item in order_items:
                            pr += item.product.price
                        return render(request, "cart.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": pr})
        
class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            basket = Order.get_basket(request.user)
            if basket:
                order_items = basket.orderitem_set.all()
                pr = 0
                for item in order_items:
                    pr += item.product.price
                return render(request, "cart.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": pr})
            else:
                return render(request, "cart.html", {"basket": None, "items": None, "count": 0, "price": 0})
        else:
            return render(request, "cart.html", {"basket": None, "items": None, "count": 0, "price":0})
            
    def post(self, request):
        type = request.POST.get("type")
        id = request.POST.get("product-id")
        href = request.POST.get("href")
        if type == "add":
            my_order = Order.objects.filter(user__id=request.user.id, status="1")
            if request.user.is_authenticated:
                if my_order.exists():
                    my_order = my_order.get()
                    OrderItem.add(my_order, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                    if href == "main":
                        return render(request, "main.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                    else:
                        pr = 0
                        for item in order_items:
                            pr += item.product.price
                        return render(request, "cart.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": pr})
                else:
                    basket = Order.create_basket(request.user)
                    OrderItem.add(basket, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                    if href == "main":
                        return render(request, "main.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                    else:
                        pr = 0
                        for item in order_items:
                            pr += item.product.price
                        return render(request, "cart.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": pr})
        elif type == "remove":
            my_order = Order.objects.filter(user__id=request.user.id, status="1")
            if request.user.is_authenticated:
                if my_order.exists():
                    my_order = my_order.get()
                    OrderItem.remove(my_order, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                    if href == "main":
                        return render(request, "main.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                    else:
                        pr = 0
                        for item in order_items:
                            pr += item.product.price
                        return render(request, "cart.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": pr})
                else:
                    basket = Order.create_basket(request.user)
                    OrderItem.remove(basket, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                    if href == "main":
                        return render(request, "main.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                    else:
                        pr = 0
                        for item in order_items:
                            pr += item.product.price
                        return render(request, "cart.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": pr})