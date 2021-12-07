from django.urls import path, include

from api import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('<username>/products', views.ProductDetail.as_view()),
    path('<username>/products/<int:id>', views.ProductDetail.as_view())
]