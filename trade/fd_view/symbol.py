from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import MetaTrader5 as mt5
from trade.fd_serializer.symbol import SymbolInfoRequestSerializer, SymbolRequestSerializer, SymbolInfoSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AllSymbolsAPIView(APIView):
    def post(self, request):
        # Validate request
        serializer = SymbolRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        login = data['login']
        password = data['password']
        server = data['server']
        path = data.get('path')

        # Initialize MT5
        if path:
            mt5.initialize(path, login=login, password=password, server=server)
        else:
            mt5.initialize(login=login, password=password, server=server)

        if not mt5.initialize():
            return Response({
                "status": "failed",
                "error": mt5.last_error()
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get all symbols
        symbols = mt5.symbols_get()
        if not symbols:
            mt5.shutdown()
            return Response({"error": "No symbols found"}, status=400)

        # Convert to dicts
        data = [s._asdict() for s in symbols]

        # Serialize response
        serializer = SymbolInfoSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        mt5.shutdown()
        return Response({
            "status": "success",
            "count": len(data),
            "symbols": serializer.data
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class SymbolInfoAPIView(APIView):
    def post(self, request):
        serializer = SymbolInfoRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        login = data['login']
        password = data['password']
        server = data['server']
        symbol = data['symbol']
        path = data.get('path')

        # Initialize MT5
        if path:
            mt5.initialize(path, login=login, password=password, server=server)
        else:
            mt5.initialize(login=login, password=password, server=server)

        if not mt5.initialize():
            return Response({
                "status": "failed",
                "error": mt5.last_error()
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get symbol info
        info = mt5.symbol_info(symbol)
        if not info:
            mt5.shutdown()
            return Response({"error": f"Symbol '{symbol}' not found"}, status=400)

        info_dict = info._asdict()

        mt5.shutdown()
        return Response(info_dict, status=200)
