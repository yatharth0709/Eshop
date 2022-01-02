from django.contrib import admin
from .models import *
# Register your models here.

class adminproduct(admin.ModelAdmin): #TO SHOW PRODUCT TABLE IN TABLE FORMAT
    list_display=['name','price','Category'] #be aware of names passed in list should be same as defined in models case sensitive


admin.site.register(Product,adminproduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)