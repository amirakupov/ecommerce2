from django.urls import path
from . import views

urlpatterns = [
	path('', views.menu, name='menu'),
	#path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('category/<int:category_id>/', views.category, name='category'),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
]