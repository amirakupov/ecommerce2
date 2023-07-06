from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.middleware import csrf
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .forms import LoginForm, UserRegistrationForm
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.db.models import Q
from .models import Product
from .models import Category
from django.contrib import messages
import stripe


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    search_query = request.GET.get('q', '')
    products = Product.objects.filter(Q(name__icontains=search_query))
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def menu(request):
    data = cartData(request)
    cartItems = data['cartItems']
    categories = Category.objects.all()
    return render(request, 'store/menu.html', {'categories': categories,
                                               'cartItems': cartItems,
                                                'section': 'menu'})

def index(request):
    return render(request, 'store/index.html')


def category(request, category_id):
    data = cartData(request)
    cartItems = data['cartItems']
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {'category': category, 'products': products, 'cartItems': cartItems})

def product_view(request, product_id):
    data = cartData(request)
    cartItems = data['cartItems']
    product = get_object_or_404(Product, id=product_id)

    wholesale_price = product.wholesale_price
    box_price = product.box_price
    minimum_quantity = product.minimum_quantity

    return render(request, 'store/product.html', {'product': product, 'cartItems': cartItems,
                                                  'wholesale_price': wholesale_price,
                                                  'box_price': box_price,
                                                  'minimum_quantity': minimum_quantity})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:

                login(request, user)
                return redirect('menu')

            else:
                return HttpResponse('Something went wrong')
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            customer = Customer.objects.create(user=new_user)
            return render(request, 'store/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
        return render(request, 'store/register.html', {'user_form': user_form})

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
        order.save()

        # Создание платежной сессии через API Stripe
        stripe.api_key = 'sk_test_51NJHjvCuKaeyCw2cLLGfS1Tk74AjBkgjLi3KLOmDYU1V3q0nOSkkjUbk4mgoEwGps1APPTI7pjgAXk7RfqoIaTeu00RTRN4ZQU'

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'unit_amount': int(total * 100),
                        'product_data': {
                            'name': 'product name',  # Название товара
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://yourwebsite.com/payment_success/',  # URL-адрес успешного завершения оплаты
                cancel_url='https://yourwebsite.com/payment_cancel/',  # URL-адрес отмены оплаты
            )

            # Получение URL-адреса платежной страницы Stripe
            payment_page_url = session.url

            # Возвращаем JSON-ответ с URL-адресом платежной страницы Stripe
            return JsonResponse({'payment_page_url': payment_page_url})
        except stripe.error.StripeError as e:
            # Обработка ошибок Stripe
            error_message = str(e)
            return JsonResponse({'error': error_message})

    return JsonResponse({'error': 'Invalid order total'})