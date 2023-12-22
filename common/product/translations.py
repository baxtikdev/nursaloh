from modeltranslation.translator import translator, TranslationOptions

from .models import Category, SubCategory, Product, CornerStatus, Brand


class CornerStatusTranslationOptions(TranslationOptions):
    fields = ['title']


translator.register(CornerStatus, CornerStatusTranslationOptions)


class BrandTranslationOptions(TranslationOptions):
    fields = ['title']


translator.register(Brand, BrandTranslationOptions)


class CategoryTranslationOptions(TranslationOptions):
    fields = ['title']


translator.register(Category, CategoryTranslationOptions)


class SubCategoryTranslationOptions(TranslationOptions):
    fields = ['title']


translator.register(SubCategory, SubCategoryTranslationOptions)


class ProductTranslationOptions(TranslationOptions):
    fields = ['title', 'description', 'material', 'brand', 'manufacturer']


translator.register(Product, ProductTranslationOptions)
