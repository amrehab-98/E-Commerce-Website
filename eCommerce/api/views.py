from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404


from .models import MyUser, Product
from .serializers import ProductSerializer, RegSerializer, UserSerializer
from api import serializers

# Create your views here.
class ProductsList(APIView):
        def get(self, request, format=None):
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

class ProductDetail(APIView):
    def get(self, request, username, id=None):
        if id:
            try:
                product = Product.objects.get(id=id)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except Product.DoesNotExist:
                raise Http404
        else:
            try:
                user = MyUser.objects.get(username=username)
                products = Product.objects.filter(owner=username)
                not_owned_products = user.get_unowned_products()
                products = products + not_owned_products
                serializer = ProductSerializer(products,many=True)
                return Response(serializer.data)
            except MyUser.DoesNotExist:
                raise Http404

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id = None):
        item = get_object_or_404(Product, id = id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})

    def put(self, request, id=None):
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
            return Response({"status": "success", "data": user.username})
        else:
            return Response({"status": "error", "data": serializer.errors})