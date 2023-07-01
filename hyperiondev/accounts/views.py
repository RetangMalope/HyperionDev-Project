from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from . models import *
from . forms import OrderForm
# Create your views here.


def home(request):
    orders = Order.objects.order_by('-date_created')[:5]  # Retrieve the last 5 orders
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = Order.objects.count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer': customer, 'orders': orders, 'order_count': order_count}
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):
    customer = Customer.objects.get(id = pk)
    form = OrderForm(initial = {'customer': customer})
    if request.method == "POST":
        
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)




def updateOrder(request, pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance = order)

    if request.method == "POST":
        form = OrderForm(request.POST, isinstance)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def DeleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    
    if request.method == "POST":
        order.delete()
        return redirect('home')
    
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)

