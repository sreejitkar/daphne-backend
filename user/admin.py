from django.contrib import admin
from .models import User,UserDetail,Shop,Slots
 

admin.site.register(User)

class UserDetailList(admin.ModelAdmin):
    list_display = [field.name for field in UserDetail._meta.get_fields()]    
admin.site.register(UserDetail,UserDetailList)

admin.site.register(Shop)    

class SlotsDetailsList(admin.ModelAdmin):
    list_display=[field.name for field in Slots._meta.get_fields()]
admin.site.register(Slots,SlotsDetailsList)    