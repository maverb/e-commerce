from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORY_CHOICES=(
    ('G','Glasses'),
    ('S','Straps'),
    ('H','Hoodie')
)

LABEL_CHOICES=(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')
)

#upload of the product by the user 
class UploadProduct(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    price=models.IntegerField(default=1000000)
    category=models.CharField(max_length=100)
    model=models.CharField(max_length=100)
    sku=models.IntegerField(default=0)
    photo=models.ImageField(default="nogenderavatar.png",upload_to="images/")


#user data    
class CreateUser(models.Model):
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password1=models.CharField(max_length=100)
    password2=models.CharField(max_length=100)

class Item(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(default="aguacates.jpg",upload_to="images/")
    price=models.FloatField()
    discount_price=models.FloatField(blank=True, null=True)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label=models.CharField(choices=LABEL_CHOICES,max_length=1)
    slug=models.SlugField() 
    description=models.TextField()

    def _str_(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })    
   
    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })
  
    def remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })
       
class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity= models.IntegerField(default=1)
    ordered=models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_price(self):
        return self.quantity * self.item.price
    
    def get_total_discount_price(self):
         return self.quantity * self.item.discount_price    

    def get_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()   
        return self.get_total_price()      
         
class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem) 
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False) 

    
    def _str_(self):
        return self.title, self.ordered

    def total_price(self):
        total=0
        for order_item in self.items.all():
            total +=order_item.get_price()
        return total 

#client data
class Client(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    shipping_address=models.CharField(max_length=100,blank=True, default='Your address')
    country=CountryField(multiple=False)
    zip_code=models.IntegerField(default='Your country')
    orders=models.ManyToManyField(Order)

