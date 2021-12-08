from django.conf.urls import url
from django.urls import path, include

from api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    url(r'^(?P<username>)[-\w.]+/products/', views.ProductsDetails.as_view()),
    url(r'^users/(?P<username>)[-\w.]+/products/(?P<id>)[0-9]+/', views.ProductsDetails.as_view()),
    path('register/', views.Users.as_view(), name='register'),
    path('orders/', views.OrdersList.as_view()),
    path('login/', obtain_auth_token, name="login")
]