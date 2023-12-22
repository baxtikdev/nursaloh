from django.contrib import admin

from .models import Category, Product, SubCategory, ProductImage

admin.site.register(SubCategory)
admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "price", "subcategory"]
    search_fields = ("code",)


admin.site.register(ProductImage)
