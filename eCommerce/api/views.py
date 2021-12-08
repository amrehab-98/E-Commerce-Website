from django.db.models import Q
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from django.shortcuts import get_object_or_404


from .models import MyUser, Product, Order
from .serializers import ProductSerializer, RegSerializer, UserSerializer, MyOrderSerializer, OrderSerializer
from rest_framework.authtoken.models import Token

# Create your views here.
class ProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class SpecificProductDetails(APIView):
    def get(self, request, username, id):
        try:
            print("hey world")
            product = Product.objects.get(id=id)
            if product.owner.username != username:
                raise Http404
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            raise Http404

class ProductsDetails(APIView):
    def get(self, request, username=None):
        try:
            print("username:", username)
            user = MyUser.objects.get(username=username)
            print(user)
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

    def post(self, request, username):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, username, id = None):
        item = get_object_or_404(Product, id = id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})

    def put(self, request, username, id=None):
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

class Users(APIView):
    def get(self, request):
        users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
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

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
            if request.user.balance >= paid_amount:
                request.user.balance -= paid_amount
                for item in serializer.validated_data['items']:
                    owner = Product.object.get(id=item.get('product').id).owner
                    owner.balance += item.get('product').price * item.get('quantity')
                    owner.save()
                request.user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": "Insufficient Balance"})       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            
        #     try:
        #         charge = stripe.Charge.create(
        #             amount=int(paid_amount * 100),
        #             currency='USD',
        #             description='Charge from Djackets',
        #             source=serializer.validated_data['stripe_token']
        #         )

        #         serializer.save(user=request.user, paid_amount=paid_amount)

        #     except Exception:
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          


        
 