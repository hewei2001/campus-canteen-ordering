from django.contrib import admin

from .models import Canteen, Shop, ShopManager


# 在admin中注册绑定
class CanteenAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['canteen_id', 'canteen_name', 'sanitation_level', 'canteen_active']


class ShopAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ['canteen__canteen_name']
    list_display = ['shop_id', 'shop_name', 'shop_active', 'manager', 'canteen']


class ShopManagerAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['manager_id', 'manager_name', 'manager_tel', 'manager_status']


admin.site.register(Canteen, CanteenAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(ShopManager, ShopManagerAdmin)

