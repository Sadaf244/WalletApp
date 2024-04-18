from django.contrib import admin
from .models import *
# Register your models here.
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

admin.site.register(BankAccount, BankAccountAdmin)

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'transaction_amount', 'transaction_date')
admin.site.register(Transactions, TransactionsAdmin)