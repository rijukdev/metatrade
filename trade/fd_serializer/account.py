from rest_framework import serializers


class AccountInfoSerializer(serializers.Serializer):
    login = serializers.IntegerField()
    password = serializers.CharField()
    server = serializers.CharField()
    path = serializers.CharField(required=False)  # optional terminal path

# Request
# {
#   "login": 95240495,
#   "password": "CrRo@6Ur",
#   "server": "MetaQuotes-Demo",
#   "path": "C:/Program Files/MetaTrader 5/terminal64.exe"
# }

# Response
# {
#     "status": "connected",
#     "login": 95240495,
#     "name": "Riju Kunbhakkudi",
#     "server": "MetaQuotes-Demo",
#     "balance": 1724.4
# }
