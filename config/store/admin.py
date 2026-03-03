from django.contrib import admin
from .models import Category,Product,Contact

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','category')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','message','created_at')


from modeltranslation.admin import TranslationAdmin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'slug')