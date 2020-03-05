from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Order, Product, Customer
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .filters import OrderFilter


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form  = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+ user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) # login method of contrib
                return redirect('home')
            else:
                messages.info(request, 'Username or Passwork incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    context = {'orders': orders[:3], 'customers': customers, 
    'pending_orders': pending_orders, 'delivered_orders': delivered_orders, 'total_orders': total_orders }
    
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {'customer': customer, 'orders': orders, 'total_orders': total_orders, 'my_filter': my_filter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'))
    customer = Customer.objects.get(id=pk)
    form = OrderFormSet(instance=customer)
    #form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        print('Printing POST', request.POST)
        #form = OrderForm(request.POST)
        form = OrderFormSet(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'formset': form}
    return render(request, 'accounts/order_form.html', context)
@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        print('Printing POST', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'formset': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect("/")
    context = {'order': order}
    return render(request, 'accounts/delete_order.html', context)