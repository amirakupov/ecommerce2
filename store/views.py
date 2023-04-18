from django.shortcuts import render

# Create your views here.
def store(request):
    context = {}
    return render(request, 'store/store.html', context)
def cart(request):
    context = {}
    return render(request, 'cart/cart.html', context)
def checkout(request):
    context = {}
    return render(request, 'checkout/checkout.html', context)