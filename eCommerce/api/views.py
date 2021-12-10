from django.db.models import Q
from django.http import Http404
from django.http.response import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from django.shortcuts import get_object_or_404
import decimal
from .models import MyUser, Product, Order, SoldProduct
from .serializers import ProductSerializer, RegSerializer, SoldProductSerializer, UserSerializer, MyOrderSerializer, OrderSerializer, PersonalInfoSerializer
from rest_framework.authtoken.models import Token
from django.conf import settings
import stripe

# Create your views here.
class MyStoreProductsList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            products = Product.objects.filter(owner=request.user.id)
            not_owned_products = request.user.get_not_owned_products()
            serializer = ProductSerializer(products,many=True)
            not_owned_serializer = ProductSerializer(not_owned_products, many=True)
            result = {}
            result['owned_products'] = serializer.data
            result['not_owned_products'] = not_owned_serializer.data
            return Response(result)
        except:
            raise HttpResponseBadRequest
    
    def put(self, request):
        product = Product.objects.get(id=request.data['id'])
        if request.user != product.owner:
            return Response({"status": "error", "data": "not authorized"})
        try:
            product.name = request.data['name']
            product.category = request.data['category']
            product.description = request.data['description']
            product.price = request.data['price']
            product.save()
            return Response({"status": "success"})
        except:
            return Response({"status": "error", "data": "error editing product"})
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        request.data['owner'] = request.user.id
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProductsList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        products = Product.objects.exclude(owner=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class SpecificProductDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, username, id):
        try:
            product = Product.objects.get(id=id)
            if product.owner.username != username:
                raise Http404
            serializer = ProductSerializer(product)
            user = MyUser.objects.get(id=request.user.id)
            userSerialized = UserSerializer(user)
            data = {}
            data['product'] = serializer.data
            data['user'] = userSerialized.data
            return Response(data)
        except Product.DoesNotExist:
            raise Http404

class ProductsDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, username=None):
        try:
            user = MyUser.objects.get(username=username)
            products = Product.objects.filter(owner=user.id)
            not_owned_products = user.get_not_owned_products()
            serializer = ProductSerializer(products,many=True)
            not_owned_serializer = ProductSerializer(not_owned_products, many=True)
            result = {}
            result['owned_products'] = serializer.data
            result['not_owned_products'] = not_owned_serializer.data
            return Response(result)
        except MyUser.DoesNotExist:
            raise Http404

class UsersList(APIView):
    # this is /stores/
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class Users(APIView):
    def post(self, request):
        print(request.data)
        serializer = RegSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            return Response({"status": "success", "token": token})
        else:
            return Response({"status": "error", "data": serializer.errors})


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # def get(self, request, format=None):
    #     orders = Order.objects.filter(user=request.user)
    #     serializer = MyOrderSerializer(orders, many=True)
    #     return Response(serializer.data)
    def get(self, request, format=None):
        products = SoldProduct.objects.filter(buyer=request.user)
        serializer = SoldProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            paid_amount = sum(item.get('price') for item in serializer.validated_data['items'])
            if request.user.balance.to_decimal() >= paid_amount:
                request.user.balance = request.user.balance.to_decimal() - paid_amount
                for item in serializer.validated_data['items']:
                    owner = Product.objects.get(id=item.get('product').id).owner
                    owner.balance = owner.balance.to_decimal() + item.get('product').price.to_decimal()
                    product =Product.objects.get(id=item.get('product').id)
                    sold_product = SoldProduct()
                    sold_product.seller = product.owner
                    sold_product.buyer = request.user
                    sold_product.category = product.category
                    sold_product.name = product.name
                    sold_product.slug=product.slug
                    sold_product.description=product.description
                    sold_product.image = product.image
                    sold_product.thumbnail=product.thumbnail
                    product.owner = request.user
                    product.price = product.price.to_decimal() + decimal.Decimal('0')
                    sold_product.price = product.price
                    sold_product.save()
                    product.save()
                    owner.save()
                request.user.save()
                serializer.save(user=request.user, paid_amount=paid_amount)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": "Insufficient Balance"}, status=status.HTTP_400_BAD_REQUEST)       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class Search(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        query = request.data.get('query', '')
        if query:
            products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
            serializer = ProductSerializer(products, many=True)
            users = MyUser.objects.filter(Q(username__icontains=query))
            serializer2 = UserSerializer(users, many=True)
            result = {}
            result['products'] = serializer.data
            result['users'] = serializer2.data
            return Response(result)
        else:
            return Response({"products": []})

# class SearchStores(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self, request):
#         query = request.data.get('query', '')

#         if query:
#             users = MyUser.objects.filter(Q(first_name__icontains=query) | Q(last_name_icontains=query) | Q(username_icontains=query))
#             serializer = UserSerializer(users, many=True)
#             return Response(serializer.data)
#         else:
#             return Response({"users": []})

class EditAndDeleteProduct(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id = None):
        item = get_object_or_404(Product, id = id)
        if request.user != item.owner:
            return Response({"status": "error", "data": "not authorized"})
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})



class PersonalInfo(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = MyUser.objects.get(id = request.user.id)
        user.balance = user.balance.to_decimal()+decimal.Decimal('0')
        print("user balance ", user.balance)
        serializer = PersonalInfoSerializer(user)  
        return Response({"status": "success", "data": serializer.data})
  
class AddBalance(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, requset):
        user = MyUser.objects.get(id = requset.user.id)
        data = requset.data
        print("data: ", data)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            charge = stripe.Charge.create(
                amount=data.get("amount"),
                currency='USD',
                description='Charge from LA Store',
                source=data.get("stripe_token")
            )
            user.balance = user.balance.to_decimal() + decimal.Decimal(data.get("amount"))
            user.save()
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"status":"error", "data":"Something went wrong. Please try again"}, 400)
        
class AddToMyStore(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        print("id: ", request.data['id'])
        product = Product.objects.get(id=request.data['id'])
        product.price = product.price.to_decimal() + decimal.Decimal('0')
        request.user.not_owned_products.add(product) 
        request.user.balance = request.user.balance.to_decimal()+decimal.Decimal('0')
        request.user.save()
        return Response({"status": "success", "data": request.data}, status.HTTP_201_CREATED)

class RemoveFromMyStore(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        product = Product.objects.get(id=request.data['id'])
        request.user.not_owned_products.remove(product) 
        request.user.balance = request.user.balance.to_decimal()+decimal.Decimal('0')
        request.user.save()
        return Response({"status": "success", "data": request.data}, status.HTTP_201_CREATED)