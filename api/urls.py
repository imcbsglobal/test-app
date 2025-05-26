from django.urls import path
from .views import HomeView, LoginView, LogoutView, IndexView, TransactionDetailsView, StockReportView, ProductsAPIView, ProductListAPIView, ProductDetailAPIView, StockCategoriesAPIView, BrandsAPIView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),        # Base URL → http://127.0.0.1:8000/
    path('home/', HomeView.as_view(), name='home'),                 
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('stock/', StockReportView.as_view(), name='stock'),
    path('transactions/', TransactionDetailsView.as_view(), name='transaction'),

    # STOCK-REPORT page API endpoints
    path('products/', ProductListAPIView.as_view(), name='api_products'),
    path('products/<str:code>/', ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('stock-categories/', StockCategoriesAPIView.as_view(), name='api_stock_categories'),
    path('brands/', BrandsAPIView.as_view(), name='api_brands'),
    path('products-list/', ProductsAPIView.as_view(), name='api_products_list'),
    
]