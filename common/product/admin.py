from django.contrib import admin

from .models import Category, Product, SubCategory, ProductImage, Uom, Brand, CornerStatus, File

admin.site.register(File)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", 'category']
    search_fields = ["title"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "price", "subcategory"]
    list_filter = ['subcategory', 'uom', 'brand', 'cornerStatus', 'isTop']
    search_fields = ["code", "title", "description"]
    inlines = [ProductImageInline]

    # def display_image(self, obj):
    #     if obj.photo:
    #         return mark_safe(f'<img src="{obj.photo.url}" width="100" height="110" />')
    #
    # display_image.short_description = 'Image'


@admin.register(Uom)
class UomAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(CornerStatus)
class CornerStatusAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]
