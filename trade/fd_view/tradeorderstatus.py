from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from trade.fd_serializer.tradeorderstatus import TradeOrderStatusBySymbolSerializer, TradeOrderStatusByTicketSerializer
import MetaTrader5 as mt5
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class TradeOrderStatusBySymbolAPIView(APIView):
    def post(self, request):
        serializer = TradeOrderStatusBySymbolSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            login = data['login']
            password = data['password']
            server = data['server']
            symbol = data.get('symbol')
            path = data.get('path')

            # Initialize MT5
            if path:
                mt5.initialize(path, login=login,
                               password=password, server=server)
            else:
                mt5.initialize(login=login, password=password, server=server)

            if not mt5.initialize():
                return Response({"status": "error", "message": "Failed to connect", "error": mt5.last_error()}, status=400)

            # Fetch open positions
            positions = mt5.positions_get(
                symbol=symbol) if symbol else mt5.positions_get()

            if not positions or len(positions) == 0:
                mt5.shutdown()
                return Response({"status": "error", "message": "No open positions found."}, status=404)

            result = []
            for pos in positions:
                result.append({
                    "ticket": pos.ticket,
                    "symbol": pos.symbol,
                    "volume": pos.volume,
                    "type": "BUY" if pos.type == mt5.ORDER_TYPE_BUY else "SELL",
                    "price_open": pos.price_open,
                    "price_current": pos.price_current,
                    "profit": pos.profit,
                    "swap": pos.swap
                    # "commission": pos.commission,
                })

            mt5.shutdown()
            return Response({"status": "success", "positions": result}, status=200)

        return Response(serializer.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class TradeOrderStatusByTicketAPIView(APIView):
    def post(self, request):
        serializer = TradeOrderStatusByTicketSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            login = data['login']
            password = data['password']
            server = data['server']
            ticket = data['ticket']
            path = data.get('path')

            # Initialize MT5 connection
            if path:
                mt5.initialize(path, login=login,
                               password=password, server=server)
            else:
                mt5.initialize(login=login, password=password, server=server)

            if not mt5.initialize():
                return Response({
                    "status": "error",
                    "message": "Failed to initialize MT5",
                    "error": mt5.last_error()
                }, status=400)

            # Fetch position by ticket
            position = mt5.positions_get(ticket=ticket)

            if position is None or len(position) == 0:
                mt5.shutdown()
                return Response({
                    "status": "error",
                    "message": f"No open position found with ticket {ticket}"
                }, status=404)

            pos = position[0]

            result = {
                "ticket": pos.ticket,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": "BUY" if pos.type == mt5.ORDER_TYPE_BUY else "SELL",
                "price_open": pos.price_open,
                "price_current": pos.price_current,
                "profit": pos.profit,
                "swap": pos.swap
                # "commission": pos.commission
            }

            mt5.shutdown()
            return Response({"status": "success", "position": result}, status=200)

        return Response(serializer.errors, status=400)
