from datetime import date, datetime, time
from os import name
from django import forms, views
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.messages.api import success
from django.db import models
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from phonenumber_field.formfields import PhoneNumberField
from phonenumbers import phonenumber
from razorpay.resources import payment
from .models import Customer, CustomerProfileForm, Product, Cart, OrderPlaced, Payment,STATE_CHOICES
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import os
from django.conf import settings
import razorpay
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


class ProductView(View):
    def get(self, request):
        tc = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L') 
        p = Product.objects.filter(stock=0)
        p.update(stc="Out of Stock")
        if request.user.is_authenticated:
            tc = len(Cart.objects.filter(user=request.user))
        return render (request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobile':mobile,'laptop':laptop,'tc':tc})


class ProductDetailView(View):
    def get(self, request, pk):
        tc = 0
        product = Product.objects.get(pk=pk)
        already_b = False
        already_c = False
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user)
            tc = len(Cart.objects.filter(user=request.user))
            already_c = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            already_b = Cart.objects.filter(Q(brand=product.brand) & Q(user=request.user)).exists()
            already_p = Cart.objects.filter(user=request.user).count()
            return render(request, 'app/productdetail.html',{'product':product,'ac':already_c,'bc':already_b,'p':already_p,'tc':tc,'cs':customer})
        else:
            return render(request, 'app/productdetail.html',{'product':product})    


# def ProductDetailViewNew(request, pk,sk):
#     return redirect('/product-detail/')


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    product_title = request.GET.get('prod_title')
    price = request.GET.get('prod_sp')
    brand = request.GET.get('prod_br')
    Cart(user=user,product=product,brand=brand,title=product_title,discounted_price=price).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        tc = 0
        tc = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        customer = Customer.objects.filter(user=request.user)
        # print(customer)
        # print(cart)
        amount = 0.0
        total = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempAmt = (p.quantity * p.product.discounted_price)
                amount += tempAmt
                total = amount
            return render(request,'app/addtocart.html',{'carts':cart,'totalAmt':total,'Amt':amount,'customer':customer,'cp':cart_product,'tc':tc,'api_key':settings.GOOGLE_MAPS_API_KEY})
        else:
            return render(request,'app/emptycart.html')    


def plus_cart(request):
    if request.method == 'GET':
        pro_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=pro_id) & Q(user=request.user))
        if c.quantity < c.product.stock:
            c.quantity+=1
            c.save()
        else:
            c.quantity+=0    
            c.save()
        amount = 0.0
        total = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        # print(cart_product)
        for p in cart_product:
            tempAmt = (p.quantity * p.product.discounted_price)
            amount += tempAmt
            total = amount
            stock = p.product.stock
        data = {
            'quantity': c.quantity,
            'Amt': amount,
            'totalAmt': total
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        pro_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=pro_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        amount = 0.0
        total = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        # print(cart_product)
        for p in cart_product:
            tempAmt = (p.quantity * p.product.discounted_price)
            amount += tempAmt
            total = amount
        data = {
            'quantity': c.quantity,
            'Amt': amount,
            'totalAmt': total
        }
        return JsonResponse(data) 

def remove_cart(request):
    if request.method == 'GET':
        pro_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=pro_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        total = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        # print(cart_product)
        for p in cart_product:
            tempAmt = (p.quantity * p.product.discounted_price)
            amount += tempAmt
        data = {
            'Amt': amount,
            'totalAmt': amount 
        }
        return JsonResponse(data)         


@login_required
def address(request):
 tc = 0
 if request.user.is_authenticated:
    tc = len(Cart.objects.filter(user=request.user))
 add = Customer.objects.filter(user=request.user)   
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary','tc':tc})

@login_required
def change_password(request):
 tc = 0
 if request.user.is_authenticated:
    tc = len(Cart.objects.filter(user=request.user))   
 return render(request, 'app/changepassword.html',{'tc':tc})

@login_required
def orders(request):
 tc = 0
 if request.user.is_authenticated:
    tc = len(Cart.objects.filter(user=request.user))   
 op = OrderPlaced.objects.filter(user=request.user) 
 return render(request, 'app/orders.html',{'op':op,'tc':tc})



def mobile(request, data=None):
 tc = 0
 if request.user.is_authenticated:
    tc = len(Cart.objects.filter(user=request.user))   
 if data == None:
     mobiles = Product.objects.filter(category='M')
    #  print(mobiles)
 elif data == 's1' or data == 's2':
     mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
     mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=1000)
 elif data == 'above':
     mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=1000)            
 return render(request, 'app/mobile.html',{'mobiles':mobiles,'tc':tc})



def meat(request, data=None):
 tc = 0
 if request.user.is_authenticated:
    tc = len(Cart.objects.filter(user=request.user))   
 if data == None:
      meats = Product.objects.filter(category='L')
 elif data == 's1' or data == 's2':
      meats = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
      meats = Product.objects.filter(category='L').filter(discounted_price__lt=1000)
 elif data == 'above':
      meats = Product.objects.filter(category='L').filter(discounted_price__gt=1000)            
 return render(request, 'app/meat.html',{'meats':meats,'tc':tc})



 
def fruit(request, data=None):
 tc = 0
 if request.user.is_authenticated:
    tc = len(Cart.objects.filter(user=request.user))   
 if data == None:
      fruits = Product.objects.filter(category='TW')
 elif data == 's1' or data == 's2':
      fruits = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
      fruits = Product.objects.filter(category='TW').filter(discounted_price__lt=1000)
 elif data == 'above':
      fruits = Product.objects.filter(category='TW').filter(discounted_price__gt=1000)            
 return render(request, 'app/fruit.html',{'fruits':fruits,'tc':tc})



 
def veg(request, data=None):
 tc = 0
 if request.user.is_authenticated:
    tc = len(Cart.objects.filter(user=request.user))   
 if data == None:
      vegs = Product.objects.filter(category='BW')
 elif data == 's1' or data == 's2':
      vegs = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
      vegs = Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
 elif data == 'above':
      vegs = Product.objects.filter(category='BW').filter(discounted_price__gt=1000)            
 return render(request, 'app/veg.html',{'vegs':vegs,'tc':tc})




class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered successfully.')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})       


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        tc = 0
        if request.user.is_authenticated:
            tc = len(Cart.objects.filter(user=request.user))
        form =CustomerProfileForm()
        # if request.user.is_authenticated:
        #     add = Customer.objects.filter(user=request.user)
        #     return render(request,'app/profile.html',{'add':add,'form':form,'active':'btn-primary'})
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary','tc':tc}) 
    def post(self, request):
        tc = 0
        if request.user.is_authenticated:
            tc = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            id = request.user.id
            usr = request.user
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(id=id,user=usr,name=name,phone_number=phone_number,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'congratulations!! Profile Updated successfully...')
        return render(request,'app/profile.html',{'form':form,'active':'btn-warning','tc':tc})



def shipping(request):
    shipping = 00.00
    if request.method == 'GET':
        pro_id = request.GET['prod_id']
        dis = request.GET['distance']
        c = Cart.objects.get(Q(product=pro_id)&Q(user=request.user))
        distance = float(dis)
        shipping = 0.0 
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        # print(cart_product)
        for p in cart_product:
            tempAmt = (p.quantity * p.product.discounted_price)
            amount += tempAmt

        # print(distance)    
        # for p in cart_product:
        #     st = 15.0
        #     shipping += st 

        if distance == 0.0:
            shipping = 17.0

        elif distance == 1.0:
            shipping = 24.0

        elif distance == 2.0:
            shipping = 31.0

        elif distance == 3.0:
            shipping = 38.0

        elif distance == 4.0:
            shipping = 44.0

        elif distance == 5.0:
            shipping = 50.0

        elif distance == 6.0:
            shipping = 56.0

        elif distance == 7.0:
            shipping = 62.0

        elif distance == 8.0:
            shipping = 68.0

        elif distance == 9.0:
            shipping = 74.0

        elif distance == 10.0:
            shipping = 80.0

        elif distance == 11.0:
            shipping = 86.0

        elif distance == 12.0:
            shipping = 92.0

        elif distance == 13.0:
            shipping = 100.0

        elif distance == 14.0:
            shipping = 150.0

        elif distance >= 15.0:
            shipping = 160.0

        p.shipping_price = shipping
        p.save()      
        data = {
            'Amt': amount,
            'totalAmt': amount + shipping,
            'shipping': shipping,
            'Distance': distance
        }
        return JsonResponse(data)
  


@login_required
def checkout(request):
    tc = 0
    if request.user.is_authenticated:
       tc = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    amount = 0.0
    total = 0.0
    sp = 0.0
    shipping = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product: 
     for p in cart_product:
            tempAmt = (p.quantity * p.product.discounted_price)
            amount += tempAmt            
     shipping = p.shipping_price
    #  print(shipping)
     if shipping == 0.0:
        return redirect('/error')  
     total = amount + shipping
     gt = total*100 
     od_id = int(gt)
    return render(request, 'app/checkout.html',{'add':add,'cart_item':cart_item,'total':total,'gt':gt,'odid':od_id,'amount':amount,'sp':shipping,'tc':tc})


def errorpage(request):
 tc = 0
 if request.user.is_authenticated:
    tc = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/error.html',{'tc':tc})


@login_required
def pay(request):
    if request.method == 'POST':
     name =  request.POST.get('name')
     amount = request.POST.get('amount')
     dam = request.POST.get('dam')
     custid = request.POST.get('custid')
     locality = request.POST.get('locality')
     phone = request.POST.get('phone')
     email = request.user.email
    #  print(name,amount,custid,locality,phone,email)
     notes = {'Shipping address': locality}
     client = razorpay.Client(auth=('rzp_test_PlEYg3Ud7QmRGo','xELzeSakL6gWRrNM2Of1wTBl'))  
     payment = client.order.create({'amount':amount, 'currency':'INR','payment_capture':1,'notes':notes})
    #  print(payment)
     pay_id = Payment(name=name,amount=dam,payment_id=payment['id']).save()
    #  print(pay_id)
     return render(request,'app/pay.html',{'order':payment,'email':email,'phone':phone,'custid':custid}) 


@csrf_exempt
def pay_success(request):
    if request.method == "POST":
        a = request.POST
        for key , val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        # print(order_id)
        user = Payment.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()    
    return payment_done(request)  
 
          
@login_required
def payment_done(request):
    user = request.user
    custid = request.POST.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, shipping_total=c.shipping_price).save()
        stock = Product.objects.filter(id=c.product.id)
        for s in stock:
            s.stock-=c.quantity 
        stock.update(stock=s.stock)
        c.delete()
    p = Product.objects.filter(stock=0)
    p.update(stc="Out of Stock")
    return redirect("orders")  
