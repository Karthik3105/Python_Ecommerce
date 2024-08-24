from knox import views as knox_views
from .views import LoginAPI, RegisterAPI, UserAPI, ChangePasswordView,index,ProductListCreateAPIView, ProductsByCategoryAPIView, ProductDetailAPIView

from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('', index, name='index'),
    path('api/products/', ProductListCreateAPIView.as_view(), name='product-list-create'),  # List all products or create a new product
    path('api/products/category/<int:category_id>/', ProductsByCategoryAPIView.as_view(), name='products-by-category'),  # Get products by category ID
    path('api/products/<int:product_id>/', ProductDetailAPIView.as_view(), name='product-detail'),  # Get product by product ID

]
