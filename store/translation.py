from modeltranslation.translator import translator, TranslationOptions
from .models import Category

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # هذا الحقل سيكون قابل للترجمة

translator.register(Category, CategoryTranslationOptions)