from rest_framework import serializers


class SymbolInfoRequestSerializer(serializers.Serializer):
    login = serializers.IntegerField()
    password = serializers.CharField()
    server = serializers.CharField()
    symbol = serializers.CharField()
    path = serializers.CharField(required=False, allow_blank=True)


class SymbolRequestSerializer(serializers.Serializer):
    login = serializers.IntegerField()
    password = serializers.CharField()
    server = serializers.CharField()
    path = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)


class SymbolInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    path = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    basis = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    isin = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    spread = serializers.IntegerField(required=False, default=0)
    digits = serializers.IntegerField(required=False, default=0)
    trade_mode = serializers.IntegerField(required=False, default=0)
    filling_mode = serializers.IntegerField(required=False, default=0)
    min_volume = serializers.FloatField(required=False, default=0.0)
    max_volume = serializers.FloatField(required=False, default=0.0)
    volume_step = serializers.FloatField(required=False, default=0.0)
    contract_size = serializers.FloatField(required=False, default=0.0)
    currency_base = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    currency_profit = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    currency_margin = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
