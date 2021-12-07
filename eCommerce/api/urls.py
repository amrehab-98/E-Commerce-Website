from django.urls import path, include

from api import views

urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('<username>/products/', views.ProductDetail.as_view()),
    path('<username>/products/<int:id>/', views.ProductDetail.as_view()),
    path('users/', views.Users.as_view()),
    path('/orders', views.OrdersList.as_view()),
]