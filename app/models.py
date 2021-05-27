from datetime import time
from django import forms
from django.db.models.enums import Choices
from django.forms import fields, widgets
from typing import DefaultDict
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.db.models.deletion import CASCADE, SET_DEFAULT, SET_NULL
from django.http import request
from phonenumber_field.modelfields import PhoneNumberField

STATE_CHOICES = (
   ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
   ('Andhra Pradesh','Andhra Pradesh'),
   ('Arunachal Pradesh','Arunachal Pradesh'),
   ('Assam','Assam'),
   ('Bihar','Bihar'),
   ('Chhattisgarh','Chhattisgarh'),
   ('Chandigarh','Chandigarh'),
   ('Dadra and Nagar Haveli','Dadra and Nagar Haveli'),
   ('Daman and Diu','Daman and Diu'),
   ('Delhi','Delhi'),
   ('Goa','Goa'),
   ('Gujarat','Gujarat'),
   ('Haryana','Haryana'),
   ('Himachal Pradesh','Himachal Pradesh'),
   ('Jammu and Kashmir','Jammu and Kashmir'),
   ('Jammu and Kashmir','Jharkhand'),
   ('Karnataka','Karnataka'),
   ('Kerala','Kerala'),
   ('Ladakh','Ladakh'),
   ('Lakshadweep','Lakshadweep'),
   ('Madhya Pradesh','Madhya Pradesh'),
   ('Maharashtra','Maharashtra'),
   ('Manipur','Manipur'),
   ('Meghalaya','Meghalaya'),
   ('Mizoram','Mizoram'),
   ('Nagaland','Nagaland'),
   ('Odisha','Odisha'),
   ('Punjab','Punjab'),
   ('Pondicherry','Pondicherry'),
   ('Rajasthan','Rajasthan'),
   ('Sikkim','Sikkim'),
   ('Tamil Nadu','Tamil Nadu'),
   ('Telangana','Telangana'),
   ('Tripura','Tripura'),
   ('Uttar Pradesh','Uttar Pradesh'),
   ('Uttarakhand','Uttarakhand'),
   ('West Bengal','West Bengal')
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(default='')
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    def __str__(self):
        return str(self.id)



CATEGORY_CHOICES = (
   ('M','Mobile'),
   ('L','Laptop'),
   ('TW','Top Wear'),
   ('BW','Bottom Wear'),
)

STOCK_CHOICES = (
   ('In Stock','In Stock'),
   ('Out of Stock','Out of Stock')
)


class Product(models.Model):
   title = models.CharField(max_length=100)
   selling_price = models.FloatField()
   discounted_price = models.FloatField()
   description = models.TextField()
   brand = models.CharField(max_length=100)
   stock = models.PositiveIntegerField(default=0)
   stc = models.CharField(choices=STOCK_CHOICES,max_length=16,default='In Stock')
   category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
   locality = models.CharField(max_length=200,default='')
   product = models.ImageField(upload_to='productimg')
   def __str__(self):
        return str(self.id)



class Cart(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   brand = models.CharField(max_length=100,null=True)
   title = models.CharField(max_length=100,default='')
   discounted_price = models.FloatField(null=True)
   shipping_price = models.FloatField(null=True,default=0)
   quantity = models.PositiveBigIntegerField(default=1)
   def __str__(self):
        return str(self.id)
   @property
   def total_cost(self):
      return self.quantity * self.product.discounted_price     



STATUS_CHOICES = (
   ('Accepted','Accepted'),
   ('Packed','Packed'),
   ('On The Way','On The Way'),
   ('Delivered','Delivered'),
   ('cancel','cancel'),
) 


class OrderPlaced(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   customer = models.ForeignKey(Customer, on_delete=CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   quantity = models.PositiveBigIntegerField(default=1)
   ordered_date = models.DateTimeField(auto_now_add=True)
   shipping_total = models.FloatField(default=0)
   status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=50)
   @property
   def total_cost(self):
      return self.quantity * self.product.discounted_price 


class CustomerProfileForm(forms.ModelForm):
   class Meta:
      model = Customer
      fields = ['name','phone_number','locality','city','state','zipcode']
      labels = {'name':'Name','locality':'Address'}
      widgets = {'name':forms.TextInput(attrs={'class':'form-control mt-2'}),'phone_number':forms.NumberInput(attrs={'class':'form-control mt-2'}),'locality':forms.TextInput(attrs={'class':'form-control mt-2'})
                ,'city':forms.TextInput(attrs={'class':'form-control mt-2'}),'state':forms.Select(attrs={'class':'form-control mt-2'})
                ,'zipcode':forms.NumberInput(attrs={'class':'form-control mt-2'})}


class Payment(models.Model):
   name = models.CharField(max_length=100)
   amount = models.CharField(max_length=100)
   payment_id = models.CharField(max_length=100)
   paid = models.BooleanField(default=False)
