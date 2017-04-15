from rest_framework import serializers
from planner.models import SimpleRule, RuleSetElement, \
   RuleSet, BaseRule, DateRule
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

class ShortSimpleRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SimpleRule
        fields = ('url', 'content', 'name_fr', 'name_en',)


class SimpleRuleSerializer(serializers.HyperlinkedModelSerializer):

    wkst = serializers.CharField(required=False, default="MO")
    byweekday = serializers.CharField(required=False, allow_blank=True, default='')
    bymonth = serializers.CharField(required=False, allow_blank=True, default='')
    bysetpos = serializers.CharField(required=False, allow_blank=True, default='')
    bymonthday = serializers.CharField(required=False, allow_blank=True, default='')
    byyearday = serializers.CharField(required=False, allow_blank=True, default='')
    byweekno = serializers.CharField(required=False, allow_blank=True, default='')
    byeaster = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_byweekday(self,value):
        weekday_pattern = "^$|^(MO|TU|WE|TH|FR|SA|SU)(\([+|-]\d\)){0,1}(,(MO|TU|WE|TH|FR|SA|SU)(\([+|-]\d\)){0,1})*$"
        if not re.match(weekday_pattern,value):
                raise serializers.ValidationError("Day not in \
                'MO','TU','WE','TH','FR','SA','SU','MO(+1)', ...")
        return value


    def validate_bymonth(self, value):
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

    def validate_byeaster(self, value):
        validation = pattern_validate(60)
        validation(value)
        return value

    class Meta:
        model = SimpleRule
        fields = (
        'url', 'content', 'name_fr', 'name_en', 'freq', 'wkst', 'byweekday', 'bymonth',
        'bysetpos', 'bymonthday', 'byyearday', 'byweekno', 'byeaster', 'next10')


class BaseRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BaseRule
        fields = ('id',)

    def to_representation(self, obj):
        if isinstance(obj, SimpleRule):
            return SimpleRuleSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, DateRule):
            return DateRuleSerializer(obj, context=self.context).to_representation(obj)
        return super(BaseRuleSerializer, self).to_representation(obj)


class ShortBaseRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BaseRule
        fields = ('id',)

    def to_representation(self, obj):
        if isinstance(obj, SimpleRule):
            return ShortSimpleRuleSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, DateRule):
            return DateRuleSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, RuleSet):
            return RuleSetSerializer(obj, context=self.context).to_representation(obj)
        return super(BaseRuleSerializer, self).to_representation(obj)

class RuleSetElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleSetElement
        fields = ('url', 'direction', 'ruleset', 'baserule', 'order')

class ShortRuleSetElementSerializer(serializers.ModelSerializer):
    baserule = ShortBaseRuleSerializer(read_only=True)
    class Meta:
        model = RuleSetElement
        fields = ('url', 'direction', 'baserule', 'order')

class RuleSetSerializer(serializers.HyperlinkedModelSerializer):
    orderedelements = ShortRuleSetElementSerializer(source='rulesetelement_set',many=True, read_only=True)
    class Meta:
        model = RuleSet
        fields = ('url', 'name_fr', 'name_en', 'orderedelements', 'next10')

class DateRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DateRule
        fields=('url','date',)
