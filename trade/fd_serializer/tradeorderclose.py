from rest_framework import serializers


class TradeOrderCloseAllBySymbolSerializer(serializers.Serializer):
    login = serializers.IntegerField()
    password = serializers.CharField()
    server = serializers.CharField()
    symbol = serializers.CharField()
    path = serializers.CharField(required=False, allow_blank=True)


class TradeOrderCloseBySymbolSerializer(serializers.Serializer):
    login = serializers.IntegerField()
    password = serializers.CharField()
    server = serializers.CharField()
    path = serializers.CharField(required=False)
    symbol = serializers.CharField()
    lot = serializers.FloatField(required=False)


class TradeOrderCloseByTicketSerializer(serializers.Serializer):
    login = serializers.IntegerField()
    password = serializers.CharField()
    server = serializers.CharField()
    path = serializers.CharField(required=False, allow_blank=True)
    ticket = serializers.IntegerField()
