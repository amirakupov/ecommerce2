from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.menu, name='menu'),
	path('index', views.index, name='index'),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('category/<int:category_id>/', views.category, name='category'),
	path('product/<int:product_id>/', views.product_view, name='product_view'),



	#authentification
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
	path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
	path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
	path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


	#registration
	path('register/', views.register, name='register'),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]