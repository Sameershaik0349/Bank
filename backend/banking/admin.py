from django.contrib import admin
from .models import BankAccount, Transaction

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'user', 'account_type', 'balance', 'is_active')
    search_fields = ('account_number', 'user__username')
    list_filter = ('account_type', 'is_active')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'account', 'timestamp')
    search_fields = ('account__account_number', 'description')
    list_filter = ('transaction_type', 'timestamp')
