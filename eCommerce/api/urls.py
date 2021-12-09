from django.conf.urls import url
from django.urls import path, include

from api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('store/', views.MyStoreProductsList.as_view()),
    path('product/<int:id>/',views.EditAndDeleteProduct.as_view()),
    path('<username>/products/', views.ProductsDetails.as_view()),
    path('<username>/products/<int:id>/', views.SpecificProductDetails.as_view()),
    path('stores/', views.UsersList.as_view()),
    path('register/', views.Users.as_view(), name='register'),
    path('orders/', views.OrdersList.as_view()),
    path('login/', obtain_auth_token, name="login"),
    path('products/search/', views.SearchProducts.as_view()),
    path('stores/search/', views.SearchStores.as_view()),
    path('user/info/', views.PersonalInfo.as_view()),
    path('account/charge/', views.AddBalance.as_view()),
]