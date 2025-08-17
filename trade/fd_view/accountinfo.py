from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from trade.fd_serializer.accountinfo import AccountInfoSerializer
import MetaTrader5 as mt5
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class AccountInfoAPIView(APIView):
    def post(self, request):
        serializer = AccountInfoSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.validated_data['login']
            password = serializer.validated_data['password']
            server = serializer.validated_data['server']
            path = serializer.validated_data.get('path', None)

            # Initialize MT5
            if path:
                initialized = mt5.initialize(
                    path, login=login, password=password, server=server)
            else:
                initialized = mt5.initialize(
                    login=login, password=password, server=server)

            if not initialized:
                return Response({
                    "status": "failed",
                    "error": mt5.last_error()
                }, status=status.HTTP_400_BAD_REQUEST)

            account = mt5.account_info()
            mt5.shutdown()

            if account:
                return Response({
                    "status": "connected",
                    "login": account.login,
                    "name": account.name,
                    "server": account.server,
                    "balance": account.balance
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "connected",
                    "message": "Login succeeded but failed to fetch account info"
                }, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
