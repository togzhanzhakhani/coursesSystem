from django.urls import path
from courses import views

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('purchase/<int:product_id>/', views.ProductPurchaseAPIView.as_view(), name='purchase-product'),
    path('products/<int:pk>/lessons/', views.LessonListAPIView.as_view(), name='product-lessons'),
]
