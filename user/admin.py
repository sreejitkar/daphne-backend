from django.contrib import admin
from .models import User,UserDetail
 

admin.site.register(User)

class UserDetailList(admin.ModelAdmin):
    list_display = [field.name for field in UserDetail._meta.get_fields()]    
admin.site.register(UserDetail,UserDetailList)
