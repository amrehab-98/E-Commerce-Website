from rest_framework import serializers
from .models import MyUser, Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "owner",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail"
        )

class UserSerializer(serializers.ModelSerializer):
    not_owned_products = ProductSerializer(many=True)
    class Meta:
        model = MyUser
        fields = (
            "id",
            "username",
            "get_name",
            "get_absolute_url",
            "not_owned_products"
        )

class RegSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type'} ,write_only=True)

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = MyUser(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'password':'Password don\'t match.'})
        user.set_password(password)
        user.save()
        return user




class MyOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )


class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "place",
            "phone",
            "items",
            "paid_amount"
        )

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "place",
            "phone",
            "items",
        )

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    

class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            "id",
            "username",
            "get_name",
            "get_absolute_url",
            "email",
            "get_balance"
        )
