from django.contrib import admin

from api.models import MyUser, Order, OrderItem, Product
from django.contrib.auth.admin import UserAdmin

#UserAdmin.fieldsets += ('Custom fields set', {'fields': ('not_owned_product', 'balance')}),

class CustomUserAdmin(UserAdmin):
    model = MyUser
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            None, {
                'fields': (
                    'not_owned_products',
                    'balance',
                )
            }
        )
    )

# Register your models here.
admin.site.register(Product)
admin.site.register(MyUser, CustomUserAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)

