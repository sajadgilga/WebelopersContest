from django.contrib import admin

# Register your models here.
from mainpage.models import UserProfile


@admin.register(UserProfile) #it is like admin.site.register(Order, OrderAdmin)
class UserAdmin(admin.ModelAdmin):
    list_display = ('bio', 'gender', 'image_tag')
    # list_filter = ('username', 'first-name',)
    # search_fields = ('username', 'first-name',)