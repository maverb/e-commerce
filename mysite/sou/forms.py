from sou.models import UploadProduct,CreateUser,Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms  
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES=(('S', 'Stripe'),
                 ('P', 'Paypal'),

                )

class UploadProductForm(forms.ModelForm):
    class Meta:
        model=UploadProduct
        fields=['name','description','price','category','model','sku','photo']

class ClientForm(forms.Form):
     shipping_address=forms.CharField(required=True, widget=forms.TextInput(attrs={
         'placeholder':'123 Main St'
     }))
     country=CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
     zip_code=forms.CharField(required=True)
     payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User    
        fields=['username','email','password1','password2']    
          