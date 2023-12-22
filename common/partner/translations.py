from modeltranslation.translator import translator, TranslationOptions

from .models import Partner


class PartnerTranslationOptions(TranslationOptions):
    fields = ['title', 'description']


translator.register(Partner, PartnerTranslationOptions)
