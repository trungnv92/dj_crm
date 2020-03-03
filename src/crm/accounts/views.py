from django.shortcuts import render
from .models import Order, Product, Customer
# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    context = {'orders': orders[:3], 'customers': customers, 
    'pending_orders': pending_orders, 'delivered_orders': delivered_orders, 'total_orders': total_orders }
    
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    context = {'customer': customer, 'orders': orders, 'total_orders': total_orders}
    return render(request, 'accounts/customer.html', context)