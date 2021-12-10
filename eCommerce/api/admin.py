from django.contrib import admin

from api.models import MyUser, Order, OrderItem, Product, SoldProduct
from django.contrib.auth.admin import UserAdmin

#UserAdmin.fieldsets += ('Custom fields set', {'fields': ('not_owned_product', 'balance')}),
class AccountAdmin(UserAdmin):
    list_display = ('first_name','last_name','email','username','get_not_owned_products','balance','date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('email','username',)
    readonly_fields=('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    # def get_not_owned_products(self, obj):
    #     return "\n".join([p.not_owned_products for p in obj.not_owned_products.all()])


# Register your models here.
admin.site.register(Product)
admin.site.register(SoldProduct)
admin.site.register(MyUser, AccountAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)

