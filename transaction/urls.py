from django.urls import path
from . import views

urlpatterns = [
    path('create-account/', views.CreateAccount.as_view()),
    path('login/', views.Login.as_view()),
    path('deposit/', views.Deposit.as_view()),
    path('withdrawal/', views.Withdrawal.as_view()),
    path('get-transaction-history/', views.TransactionHistory.as_view()),
    path('get-wallet-balance/', views.GetWalletBalance.as_view())
    ]