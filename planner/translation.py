from modeltranslation.translator import register, TranslationOptions
from .models import SimpleRule, RuleSet

@register(SimpleRule)
class SimpleRuleTranslation(TranslationOptions):
    fields = ('name',)

@register(RuleSet)
class RuleSetTranslation(TranslationOptions):
    fields = ('name',)
