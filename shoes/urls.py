from django.urls import path
from shoes import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('cart/', views.CartView.as_view(), name="cart"),
]