from http.client import HTTPResponse
from django.http import  JsonResponse
from shopkart.form import CustomUserFrom
from django.shortcuts import redirect,render
from . models import *
import json
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    Products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"Products":Products})


def favviewpage(request):
   if request.user.is_authenticated:
      fav=Favourite.objects.filter(user=request.user)
      return render(request,"shop/fav.html",{"fav":fav})
   else:
      return redirect("/")


def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpage")





def cart_page(request):
   if request.user.is_authenticated:
      cart=Cart.objects.filter(user=request.user)
      return render(request,"shop/cart.html",{"cart":cart})
   else:
      return redirect("/")

def remove_cart(request,cid):
    cart_item=Cart.objects.get(id=cid)
    cart_item.delete()
    return redirect("/cart")

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
      if request.user.is_authenticated:
        data=json.load(request)
        Product_id=data['pid']
        #  print(request.user.id)
        product_status=Product.objects.get(id=Product_id)
        if product_status:
            if Favourite.objects.filter(user=request.user.id,Product_id=Product_id):
               return JsonResponse({'status':'Product Already in Favourite'}, status=200)
            else:
                Favourite.objects.create(user=request.user,Product_id=Product_id)
                return JsonResponse({'status':'Product Added to Favourite Success '}, status=200)
      else:
        return JsonResponse({'status':'Login To Add Favourite'}, status=200)              
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)






   

   
















def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
      if request.user.is_authenticated:
        data=json.load(request)
        product_qty=data['product_qty']
        Product_id=data['pid']
        #  print(request.user.id)
        product_status=Product.objects.get(id=Product_id)
        if product_status:
            if Cart.objects.filter(user=request.user.id,Product_id=Product_id):
               return JsonResponse({'status':'Product Already in Cart'}, status=200)
            else:
               if product_status.quanitity>=product_qty:
                Cart.objects.create(user=request.user,Product_id=Product_id,product_qty=product_qty)
                return JsonResponse({'status':'Product Add to cart Success '}, status=200)
               else:
                return JsonResponse({'status':'Product Stack Not Available'}, status=200)             
      else:
        return JsonResponse({'status':'Login To Add Cart'}, status=200)              
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)





def logout_page(request):
    if request.user.is_authenticated:
      logout(request)
      messages.success(request,"Logged out Successfully")
      return redirect("/")  
   


def login_page(request):
    if request.user.is_authenticated:
       return redirect("/")
    else:
        if request.method=='POST' :
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successsfully")
                return redirect("/")
            else:
                messages.error(request,"Invaild User Name or Password")
                return redirect("/login")   
        return render(request,"shop/login.html")


def register(request):
    form=CustomUserFrom()
    if request.method=='POST' :
       form=CustomUserFrom(request.POST)
       if form.is_valid():
          form.save()
          messages.success(request,"Registration Success You Can Login Now...!!!")
          return redirect('/login') 
    return render(request, "shop/register.html",{'form':form})

def Collection(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"shop/Collection.html",{"catagory":catagory})


def Collectionsview(request,name):
    if(Catagory.objects.filter(name=name, status=0)):
        Products=Product.objects.filter(Catagory__name=name)
        return render(request,"shop/products/index.html",{"Products":Products,"catagory_name":name})
    else:
        messages.warning(request,"NO such catagory Found")
        return redirect('Collection')


def Product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        Products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"shop/products/Product_details.html",{"Products":Products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('Collection')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('Collection')
