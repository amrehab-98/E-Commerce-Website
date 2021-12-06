from django.contrib import admin

from api.models import Category, MyUser, Order, OrderItem, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(MyUser)
admin.site.register(Order)
admin.site.register(OrderItem)

