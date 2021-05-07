from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import CreateUser,Item,OrderItem,Order
from .forms import CreateUserForm,ClientForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User 
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView,DetailView,View,TemplateView
from django.utils import timezone 
from django.conf import settings 
import json
from django.http import JsonResponse



def checkout(request):
    order=Order.objects.get(user=request.user,ordered=False)
    context={ 
        'order':order,
     }    
    return render(request,'checkout-page.html',context)

def paymentComplete(request):
  order=Order.objects.get(user=request.user,ordered=False)
  order_item=OrderItem.objects.filter(user=request.user).all()
  body=json.loads(request.body)
  if body:
     order.ordered=True 
     order.save(update_fields=['ordered'])
     order.delete()
     order_item.delete()
     print(order_item)
  else:
    print("order not found")   
  return JsonResponse('Payment completed!',safe=False)
  
#list view to display the products
class HomeView(ListView):
   model=Item
   template_name="home-page.html"   

#view of the description of the product
class ItemDetailView(DetailView):
  model=Item
  template_name="product.html"

#view of the payment are
class PaymentView(View):
  def get(self,*args,**kwargs):
    return render(self.request,"payment.html")

#a view to handle the car once you add products
def cart(request):
     try:
        orders=Order.objects.get(user=request.user,ordered=False)
        context={
          'orders':orders,
        }
        return render(request,'cart.html',context)   
     except ObjectDoesNotExist:
         messages.error(request,"You dont have any order yet")
         return HttpResponseRedirect("home.html")     

#adding a product to the cart
def add_to_cart(request,slug):
   item=get_object_or_404(Item,slug=slug)
   order_item, created = OrderItem.objects.get_or_create(
       item=item,
       user=request.user,
       ordered=False
   )
   order_qs=Order.objects.filter(user=request.user,ordered=False)
   if order_qs.exists():
     order=order_qs[0]
     #check if it is has been already ordered
     if order.items.filter(item__slug=item.slug).exists():
       order_item.quantity += 1
       order_item.save()
       return HttpResponseRedirect('/cart/') 
     else:
       order.items.add(order_item) 
       return HttpResponseRedirect('/cart/') 
   else:
     ordered_date=timezone.now()
     order=Order.objects.create(user=request.user,ordered_date=ordered_date)
     order.items.add(order_item)
     return HttpResponseRedirect('/cart/')
   return redirect("product", slug=slug)  

def remove_from_cart(request,slug):
     item=get_object_or_404(Item,slug=slug)
     order_qs=Order.objects.filter(user=request.user,ordered=False)
     if order_qs.exists():
        order=order_qs[0]
        #check if it is has been ordered already
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                        item=item,
                        user=request.user,
                        ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
        else:
           messages.info(request,"This item was not in your cart")
           return redirect("product",slug=slug)
     else:
          messages.info(request,"The user does not have any order")
          return redirect("product",slug=slug) 
     return redirect("cart")

#just a regular login view
@csrf_exempt
def loginPage(request):
  ur=user.request
  context={
  }
  if request.method=='POST':
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(request,username=username,password=password)
    if user is not None:
      ur=request.user
      context={
          'ur':ur,
          'object_list':Item.objects.all(),
      } 
      login(request,user)
      return render(request,'home-page.html', context)
    else:
      messages.warning(request,'Incorrect user or password')    
  return render(request,'login.html', context)

#just a regular logout view
@login_required
def logout(request): 
   django_logout(request)
   context={
   }
   #return render(request,"bookings/home.html",context)
   return HttpResponseRedirect('/login_1234saju/') 

#just a regular register view
def register(request):
  form=CreateUserForm(request.POST or None)
  if form.is_valid():
    form.save()
    messages.success(request,'Your account was created!')
    return redirect('/login')
  context={
        'form':form
  } 
  return render(request,'register.html',context) 


