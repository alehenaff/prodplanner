from modeltranslation.translator import register, TranslationOptions
from .models.models import SimpleRule

@register(SimpleRule)
class SimpleRuleTranslation(TranslationOptions):
    fields = ('name',)
