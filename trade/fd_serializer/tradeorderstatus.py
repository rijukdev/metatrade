from rest_framework import serializers


class TradeOrderStatusBySymbolSerializer(serializers.Serializer):
    login = serializers.IntegerField()
    password = serializers.CharField()
    server = serializers.CharField()
    symbol = serializers.CharField(required=False)
    path = serializers.CharField(required=False)


class TradeOrderStatusByTicketSerializer(serializers.Serializer):
    login = serializers.IntegerField()
    password = serializers.CharField()
    server = serializers.CharField()
    ticket = serializers.IntegerField()
    path = serializers.CharField(required=False)
