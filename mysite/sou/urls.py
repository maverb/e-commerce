from django.urls import path 

from . import views 

from sou.views import (HomeView,
                       ItemDetailView,
                       PaymentView,
                       )


urlpatterns=[
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/',views.add_to_cart, name='add-to-cart'),
     path('remove-from-cart/<slug>/',views.remove_from_cart, name='remove-from-cart'),
    path('register/',views.register,name='register'),
    path('checkout-page/',views.checkout,name='checkout-page'),
    path('login/',views.loginPage,name='loginPage'),
    path('register/',views.register,name='register'),
    path('cart/',views.cart,name='cart'),
    path('payment/<payment_option>/',PaymentView.as_view(), name='payment'),
    path('complete/',views.paymentComplete,name='complete'),
]

