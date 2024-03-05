from django.contrib import admin
from  .models import Catagory
from .models import Product
from .models import *
# Register your models here.

# class CatagoryAdmin(admin.ModelAdmin):
#     list_display =('name','image','description','status')
# admin.site.register(Catagory,CatagoryAdmin)    



admin.site.register(Catagory)
admin.site.register(Product)
