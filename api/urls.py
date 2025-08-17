from django.urls import path, include
from trade import views as metatradeView


urlpatterns = [
    path('metatrade/account-info/',
         metatradeView.AccountInfoAPIView.as_view(), name='mt5-account-info'),

    path('metatrade/trade-order/',
         metatradeView.TradeOrderAPIView.as_view(), name='mt5-trade-order'),

    path('metatrade/trade-order-status-symbol/',
         metatradeView.TradeOrderStatusBySymbolAPIView.as_view(), name='mt5-trade-order-status-symbol'),

    path('metatrade/trade-order-status-ticket/',
         metatradeView.TradeOrderStatusByTicketAPIView.as_view(), name='mt5-trade-order-status-ticket'),

    path('metatrade/trade-order-close-all-symbol/',
         metatradeView.TradeOrderCloseAllBySymbolAPIView.as_view(), name='mt5-trade-order-close-all-symbol'),

    path('metatrade/trade-order-close-symbol/',
         metatradeView.TradeOrderCloseBySymbolAPIView.as_view(), name='mt5-trade-order-close-symbol'),

    path('metatrade/trade-order-close-ticket/',
         metatradeView.TradeOrderCloseByTicketAPIView.as_view(), name='mt5-trade-order-close-ticket'),
]
