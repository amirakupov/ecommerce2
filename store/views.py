from django.shortcuts import render, get_object_or_404
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse
import json
import datetime
from django.db.models import Q
from .models import Product
from .models import Category


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
    return render(request, 'store/menu.html', {'categories': categories, 'cartItems': cartItems})

def category(request, category_id):
    data = cartData(request)
    cartItems = data['cartItems']
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {'category': category, 'products': products, 'cartItems': cartItems})

def login_view(request):

    return render(request, 'store/login.html')

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

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    print("Data", request.body)
    return JsonResponse('Payment complete', safe=False)
