from django.contrib import admin
# from django.utils.translation import gettext_lazy as _
from .models import Restaurant, Category, MenuItem, Order, OrderItem, Review, Deal, Reward

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'rating', 'created_on')

class RestaurantDomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'restaurant', 'is_primary')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price')

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'restaurant', 'total', 'status',)
    inlines = [OrderItemInline]
    actions = ['mark_as_ready_for_delivery', 'mark_as_delivered']

    # def mark_as_ready_for_delivery(self, request, queryset):
    #     updated = queryset.update(status='READY')
    #     self.message_user(request, _(f'{updated} orders have been marked as ready for delivery.'))
    # mark_as_ready_for_delivery.short_description = _('Mark selected orders as ready for delivery')
    #
    # def mark_as_delivered(self, request, queryset):
    #     updated = queryset.update(status='DELIVERED')
    #     self.message_user(request, _(f'{updated} orders have been marked as delivered.'))
    # mark_as_delivered.short_description = _('Mark selected orders as delivered')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'restaurant', 'rating', 'comment',)

class DealAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'title', 'description', 'start_date', 'end_date')

class RewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(Reward, RewardAdmin)
