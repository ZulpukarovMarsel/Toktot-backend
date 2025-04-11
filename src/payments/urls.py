from django.urls import path
from .views import CardsView, TopUpBalanceView

urlpatterns = [
    path('cards/', CardsView.as_view(), name='get-create-cards'),
    path('topup/', TopUpBalanceView.as_view(), name='topup-balance'),
]
