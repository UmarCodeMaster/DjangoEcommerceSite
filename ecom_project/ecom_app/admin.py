from django.contrib import admin
# Register your models here.
from .models import Category,Product,Company,Image,ProductReview,Shipping,CheckoutCart,CartItem
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Company)
admin.site.register(Image)
admin.site.register(Shipping)
admin.site.register(CheckoutCart)
admin.site.register(CartItem)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','product', 'rating', 'created_at')
    readonly_fields = ['created_at']