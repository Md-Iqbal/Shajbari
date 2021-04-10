from django.contrib import admin
from .models import *

# Register your models here.


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at', 'status']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject', 'update_at', 'status']
    readonly_fields = ('name','email','subject','message','ip')
    list_filter=['status']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'ordernumber', 'status', 'update_at']
    list_filter = ['status']


admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ, FAQAdmin)
