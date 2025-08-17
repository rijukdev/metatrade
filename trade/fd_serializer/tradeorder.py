from rest_framework import serializers


class TradeOrderSerializer(serializers.Serializer):
    # place order
    login = serializers.IntegerField()
    password = serializers.CharField()
    server = serializers.CharField()
    path = serializers.CharField(required=False)

    symbol = serializers.CharField()
    volume = serializers.FloatField()
    order_type = serializers.ChoiceField(choices=[
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ])
    price = serializers.FloatField(required=False)
    sl = serializers.FloatField(required=False)  # Stop Loss
    tp = serializers.FloatField(required=False)  # Take Profit

# {
#   "login": 95240495,
#   "password": "CrRo@6Ur",
#   "server": "MetaQuotes-Demo",
#   "path": "C:/Program Files/MetaTrader 5/terminal64.exe",
#   "symbol": "BTCUSD",
#   "volume": 0.5,
#   "order_type": "sell" #   "order_type": "buy"
# }
