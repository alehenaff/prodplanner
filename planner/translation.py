from modeltranslation.translator import register, TranslationOptions
from .models import DayTemplateRule, RuleSet

@register(DayTemplateRule)
class SimpleRuleTranslation(TranslationOptions):
    fields = ('name',)

@register(RuleSet)
class RuleSetTranslation(TranslationOptions):
    fields = ('name',)
