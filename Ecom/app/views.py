from django.shortcuts import render,redirect
from .models import *
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
#def home(request):
#return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
       topwears=Product.objects.filter(category='TW')
       bottomwears=Product.objects.filter(category='BW')
       mobiles=Product.objects.filter(category='M')
       laptops=Product.objects.filter(category='L')
       return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops })

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
          item_already_in_cart=Cart.objects.filter(Q(product=product.id)& Q(user=request.user)
                                                   ).exists()
          return render(request,'app/productdetail.html',{'product':product,
                                                          'item_already_in_cart':item_already_in_cart})
        else:
          return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

def add_to_cart(request):
  user=request.user
  product_id=request.GET.get('prod_id')
  product=Product.objects.get(id=product_id)
  Cart(user=user, product=product).save()
  return redirect('/cart/')


def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

def login(request):
 return render(request, 'app/login.html')

def customerregistration(request):
 return render(request, 'app/customerregistration.html')

def checkout(request):
 return render(request, 'app/checkout.html')

def show_cart(request):
  if request.user.is_authenticated:
    user= request.user
    cart=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==user]
    print(cart_product)
    if cart_product:
      for p in cart_product:
        tempamount=(p.quantity*p.product.discounted_price)
        amount +=tempamount
        total_amount=amount+shipping_amount
      return render(request, 'app/addtocart.html',{'carts':cart, 'total_amount':total_amount,'amount':amount})
    else:
      return render(request,'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)



def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'ZARA' or data == 'GUCCI':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(
            category='TW').filter(discounted_price__lt=1000)
    elif data == 'above':
        topwears = Product.objects.filter(
            category='TW').filter(discounted_price__gt=1000)
    return render(request, 'app/topwear.html', {'topwears': topwears})

def bottomwear(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'ZARA' or data == 'GUCCI':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwears = Product.objects.filter(
            category='BW').filter(discounted_price__lt=1000)
    elif data == 'above':
        bottomwears = Product.objects.filter(
            category='BW').filter(discounted_price__gt=1000)
    return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears})

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Asus' or data == 'Dell':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(
            category='L').filter(discounted_price__lt=25000)
    elif data == 'above':
        laptops = Product.objects.filter(
            category='L').filter(discounted_price__gt=25000)
    return render(request, 'app/laptop.html', {'laptops': laptops})



