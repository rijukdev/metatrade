from django.shortcuts import render

from .fd_view.account import AccountInfoAPIView
from .fd_view.symbol import SymbolInfoAPIView, AllSymbolsAPIView
from .fd_view.tradeorder import TradeOrderAPIView
from .fd_view.tradeorderclose import TradeOrderCloseAllBySymbolAPIView, TradeOrderCloseBySymbolAPIView, TradeOrderCloseByTicketAPIView
from .fd_view.tradeorderstatus import TradeOrderStatusBySymbolAPIView, TradeOrderStatusByTicketAPIView
