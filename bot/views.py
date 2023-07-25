from bot.forms import PaymentForm
import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, Cart, ProductInOrder


# Create your views here.

def payment(request):
    return render(request, 'pages/payment.html')


def faqs(request):
    return render(request, 'pages/faqs.html')


def create_account(request):
    return render(request, 'pages/create_account.html')


def catalog(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search')

    products = Product.objects.filter(quantity__gt=0)

    if category:
        products = products.filter(category__pk=category)

    if search_query:
        products = products.filter(category__name__icontains=search_query)

    order_by = request.GET.get('order_by')

    if order_by:
        products = products.order_by(order_by)
    else:
        products = products.order_by('name')

    categories = Category.objects.all()

    return render(request, 'pages/catalog.html', {'products': products, 'categories': categories})


# def detail(request, pk):
#     products = Product.objects.order_by('?')[:4]
#     product = get_object_or_404(Product, pk=pk)
#     print(product.quantity)
#     return render(request, 'pages/detail.html', context={'product': product, 'products': products})
def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Получите список товаров, которые относятся к той же категории, что и текущий товар
    products = Product.objects.filter(category=product.category)
    # .exclude(pk=pk)[:4]

    return render(request, 'pages/detail.html', context={'product': product, 'products': products})


def save_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save_and_send_to_telegram()
            return JsonResponse({'success': True})
        else:
            return JsonResponse(
                {'error': 'Пожалуйста, заполните все поля и согласитесь с политикой конфиденциальности, офертой!'})
