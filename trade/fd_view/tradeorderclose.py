from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from trade.fd_serializer.tradeorderclose import TradeOrderCloseAllBySymbolSerializer, TradeOrderCloseBySymbolSerializer, TradeOrderCloseByTicketSerializer
import MetaTrader5 as mt5
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class TradeOrderCloseAllBySymbolAPIView(APIView):
    def post(self, request):
        serializer = TradeOrderCloseAllBySymbolSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        login = data['login']
        password = data['password']
        server = data['server']
        symbol = data['symbol']
        path = data.get('path', '')

        # Initialize MT5
        if path:
            initialized = mt5.initialize(
                path, login=login, password=password, server=server)
        else:
            initialized = mt5.initialize(
                login=login, password=password, server=server)

        if not initialized:
            return Response({
                "status": "error",
                "message": "MT5 initialization failed",
                "error": mt5.last_error()
            }, status=500)

        # Get all positions for the given symbol
        positions = mt5.positions_get(symbol=symbol)
        if not positions:
            mt5.shutdown()
            return Response({
                "status": "error",
                "message": f"No active positions found for {symbol}"
            }, status=404)

        # Ensure symbol is available
        if not mt5.symbol_select(symbol, True):
            mt5.shutdown()
            return Response({
                "status": "error",
                "message": f"Failed to select symbol {symbol}"
            }, status=500)

        # Get symbol info for filling mode
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            mt5.shutdown()
            return Response({
                "status": "error",
                "message": f"Symbol info not found for {symbol}"
            }, status=404)

        results = []
        for pos in positions:
            volume = pos.volume
            order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(
                symbol).bid if pos.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask

            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "position": pos.ticket,
                "price": price,
                "deviation": 20,
                "magic": 1000,
                "comment": "Close trade by symbol API",
                "type_time": mt5.ORDER_TIME_GTC,
            }

            # Try all filling modes
            trade_result = None
            for filling in [symbol_info.filling_mode, mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_RETURN]:
                close_request["type_filling"] = filling
                result = mt5.order_send(close_request)
                if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                    trade_result = {
                        "ticket_closed": result.order,
                        "retcode": result.retcode,
                        "comment": result.comment
                    }
                    break

            if trade_result is None:
                trade_result = {
                    "ticket": pos.ticket,
                    "status": "failed",
                    "last_error": mt5.last_error()
                }

            results.append(trade_result)

        mt5.shutdown()

        return Response({
            "status": "completed",
            "symbol": symbol,
            "results": results
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class TradeOrderCloseBySymbolAPIView(APIView):
    def post(self, request):
        serializer = TradeOrderCloseBySymbolSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            login = data['login']
            password = data['password']
            server = data['server']
            path = data.get('path', None)
            symbol = data['symbol']
            lot = data.get('lot', None)

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

            # Get open positions for the symbol
            positions = mt5.positions_get(symbol=symbol)
            if not positions or len(positions) == 0:
                mt5.shutdown()
                return Response({"error": f"No open positions found for {symbol}"}, status=404)

            position = positions[0]
            order_type = mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY

            # Get price
            tick = mt5.symbol_info_tick(symbol)
            if not tick:
                mt5.shutdown()
                return Response({"error": f"Price tick not found for {symbol}"}, status=500)

            price = tick.bid if order_type == mt5.ORDER_TYPE_SELL else tick.ask
            volume = lot or position.volume

            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": position.ticket,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "deviation": 10,
                "magic": 100234,
                "comment": "Close order via Django API",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(close_request)
            mt5.shutdown()

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                return Response({
                    "status": "error",
                    "retcode": result.retcode,
                    "comment": result.comment
                }, status=400)

            return Response({
                "status": "success",
                "closed_ticket": position.ticket,
                "symbol": symbol,
                "volume": volume
            }, status=200)

        return Response(serializer.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class TradeOrderCloseByTicketAPIView(APIView):
    def post(self, request):
        serializer = TradeOrderCloseByTicketSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        login = data['login']
        password = data['password']
        server = data['server']
        ticket = data['ticket']
        path = data.get('path', '')

        # Initialize MT5
        if path:
            initialized = mt5.initialize(
                path, login=login, password=password, server=server)
        else:
            initialized = mt5.initialize(
                login=login, password=password, server=server)

        if not initialized:
            return Response({
                "status": "error",
                "message": "MT5 initialization failed",
                "error": mt5.last_error()
            }, status=500)

        # Get position by ticket
        position = mt5.positions_get(ticket=ticket)
        if not position:
            mt5.shutdown()
            return Response({
                "status": "error",
                "message": f"No active position found for ticket {ticket}"
            }, status=404)

        pos = position[0]
        symbol = pos.symbol
        volume = pos.volume
        order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(
            symbol).bid if pos.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask

        # Ensure symbol is available
        if not mt5.symbol_select(symbol, True):
            mt5.shutdown()
            return Response({
                "status": "error",
                "message": f"Failed to select symbol {symbol}"
            }, status=500)

        # Detect broker's filling mode
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            mt5.shutdown()
            return Response({
                "status": "error",
                "message": f"Symbol info not found for {symbol}"
            }, status=404)

        # Prepare base request
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": 1000,
            "comment": "Close trade by API",
            "type_time": mt5.ORDER_TIME_GTC,
        }

        # Try all possible filling modes until success
        for filling in [symbol_info.filling_mode, mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_RETURN]:
            close_request["type_filling"] = filling
            result = mt5.order_send(close_request)
            if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                mt5.shutdown()
                return Response({
                    "status": "success",
                    "ticket_closed": result.order,
                    "retcode": result.retcode,
                    "comment": result.comment
                }, status=200)

        # If all modes failed
        mt5.shutdown()
        return Response({
            "status": "error",
            "message": "Failed to close trade with all filling modes",
            "last_error": mt5.last_error(),
            "last_result": result._asdict() if result else None
        }, status=400)
