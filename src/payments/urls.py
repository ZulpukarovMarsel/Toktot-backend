from django.urls import path
from .views import ChargeWithSavedCardView, PayPalCardsView

urlpatterns = [
    path('paypal/cards/charge/', ChargeWithSavedCardView.as_view(), name='charge-with-saved-card'),
    path('paypal/cards/', PayPalCardsView.as_view(), name='paypal-cards-list-add'),
]
