from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from trade.fd_serializer.tradeorder import TradeOrderSerializer
import MetaTrader5 as mt5
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class TradeOrderAPIView(APIView):
    def post(self, request):
        serializer = TradeOrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            login = data['login']
            password = data['password']
            server = data['server']
            path = data.get('path', None)

            symbol = data['symbol']
            volume = data['volume']
            order_type = data['order_type']
            sl = data.get('sl')
            tp = data.get('tp')

            # Initialize MT5
            if path:
                mt5.initialize(path, login=login,
                               password=password, server=server)
            else:
                mt5.initialize(login=login, password=password, server=server)

            if not mt5.initialize():
                return Response({
                    "status": "failed",
                    "error": mt5.last_error()
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if symbol exists
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                mt5.shutdown()
                return Response({"error": f"Symbol '{symbol}' not found"}, status=400)

            # If symbol is not visible, make it visible
            if not symbol_info.visible:
                mt5.symbol_select(symbol, True)

            # Get current price
            tick = mt5.symbol_info_tick(symbol)
            if not tick:
                mt5.shutdown()
                return Response({"error": f"Could not get price for '{symbol}'"}, status=400)

            price = tick.ask if order_type == 'buy' else tick.bid
            order_type_enum = mt5.ORDER_TYPE_BUY if order_type == 'buy' else mt5.ORDER_TYPE_SELL

            # 🔑 Force filling mode = 1 (IOC)
            filling_mode = mt5.ORDER_FILLING_IOC

            request_order = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type_enum,
                "price": price,
                "sl": sl if sl else 0.0,
                "tp": tp if tp else 0.0,
                "deviation": 10,
                "magic": 100234,
                "comment": "Order from Django API",
                "type_time": mt5.ORDER_TIME_GTC,
                # "type_filling": filling_mode,
            }

            result = mt5.order_send(request_order)
            mt5.shutdown()

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                return Response({
                    "status": "error",
                    "retcode": result.retcode,
                    "comment": result.comment
                }, status=400)

            return Response({
                "status": "success",
                "order_id": result.order,
                "symbol": symbol,
                "volume": volume,
                "price": price,
                "filling_mode": filling_mode
            }, status=200)
        return Response(serializer.errors, status=400)
