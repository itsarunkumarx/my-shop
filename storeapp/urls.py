from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/update/<int:id>/', views.product_update, name='product_update'),
    path('product/delete/<int:id>/', views.product_delete, name='product_delete'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-success/<int:id>/', views.order_success, name='order_success'),
    path('order-detail/<int:id>/', views.order_detail, name='order_detail'),
    path('review/<int:id>/', views.add_review, name='add_review'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]


