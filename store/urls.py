from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.menu, name='menu'),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('category/<int:category_id>/', views.category, name='category'),
	path('login/', views.login_view, name='login'),
	path('index', views.index, name='index'),
	#path('login/', auth_views.LoginView.as_view(), name='login'),
	#path('logout/', auth_views.LogoutView.as_view(), name='logout'),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
]