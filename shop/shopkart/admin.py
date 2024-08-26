# from atexit import register
from django.contrib import admin
from .models import *
# Register your models here.

# class CatagoryAdmin(admin.ModelAdmin):
#     list_display =('name','image','description','status')
# admin.site.register(Catagory,CatagoryAdmin)    



admin.site.register(Catagory)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Favourite)