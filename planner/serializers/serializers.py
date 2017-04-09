from rest_framework import serializers
from planner.models.models import SimpleRule, RuleSetElement, \
   RuleSet, BaseRule, DateTimeRule
import re

def pattern_validate(nbmax):
    """
    returns a validator function for an interger
    or a list of integers ; the length of the list
    is lower than nbmax+2
    """
    def validate(value):
        pattern = "^(-?\d{1,2}(,-?\d{1,2}){0,"+str(nbmax)+"})?$"
        if not re.match(pattern,value) :
            raise serializers.ValidationError("Doesn't respect pattern : \
            integer or sequence of integers (comma separated)")
    return validate


class SimpleRuleSerializer(serializers.HyperlinkedModelSerializer):

    wkst = serializers.CharField(required=False, default="MO")
    byweekday = serializers.CharField(required=False, allow_blank=True, default='')
    bymonth = serializers.CharField(required=False, allow_blank=True, default='')
    bysetpos = serializers.CharField(required=False, allow_blank=True, default='')
    bymonthday = serializers.CharField(required=False, allow_blank=True, default='')
    byyearday = serializers.CharField(required=False, allow_blank=True, default='')
    byweekno = serializers.CharField(required=False, allow_blank=True, default='')
    byhour = serializers.CharField(required=False, allow_blank=True, default='0', initial='0')
    byminute = serializers.CharField(required=False, allow_blank=True, default='0', initial='0')
    bysecond = serializers.CharField(required=False, allow_blank=True, default='0', initial='0')
    byeaster = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_byweekday(self,value):
        weekday_pattern = "^$|^(MO|TU|WE|TH|FR|SA|SU)(\([+|-]\d\)){0,1}(,(MO|TU|WE|TH|FR|SA|SU)(\([+|-]\d\)){0,1})*$"
        if not re.match(weekday_pattern,value):
                raise serializers.ValidationError("Day not in \
                'MO','TU','WE','TH','FR','SA','SU','MO(+1)', ...")
        return value


    def validate_month(self, value):
        validation = pattern_validate(12)
        validation(value)
        return value

    def validate_bysetpos(self, value):
        validation = pattern_validate(15)
        validation(value)
        return value

    def validate_bymonthday(self, value):
        validation = pattern_validate(31)
        validation(value)
        return value

    def validate_byyearday(self, value):
        validation = pattern_validate(365)
        validation(value)
        return value

    def validate_byweekno(self, value):
        validation = pattern_validate(52)
        validation(value)
        return value

    def validate_byhour(self, value):
        validation = pattern_validate(24)
        validation(value)
        return value

    def validate_byminute(self, value):
        validation = pattern_validate(60)
        validation(value)
        return value

    def validate_bysecond(self, value):
        validation = pattern_validate(60)
        validation(value)
        return value

    def validate_byeaster(self, value):
        validation = pattern_validate(60)
        validation(value)
        return value

    class Meta:
        model = SimpleRule
        fields = (
        'url', 'content', 'name_fr', 'name_en', 'freq', 'wkst', 'byweekday', 'bymonth',
        'bysetpos', 'bymonthday', 'byyearday', 'byweekno', 'byhour', 'byminute',
        'bysecond', 'byeaster', 'next10')


class RuleSetElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleSetElement
        fields = ('url', 'direction', 'ruleset', 'baserule', 'order')

class RuleSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RuleSet
        fields = ('url', 'name', 'elements',)


class BaseRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BaseRule
        fields = ('id',)

    def to_representation(self, obj):
        if isinstance(obj, SimpleRule):
            return SimpleRuleSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, DateTimeRule):
            return DateTimeRuleSerializer(obj, context=self.context).to_representation(obj)
        return super(BaseRuleSerializer, self).to_representation(obj)

class DateTimeRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DateTimeRule
        fields=('url','datetime',)
