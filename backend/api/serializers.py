from rest_framework import serializers
from banking.models import BankAccount, Transaction
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number')

class BankAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = BankAccount
        fields = ('id', 'user', 'account_number', 'account_type', 'balance', 'created_at')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'account', 'transaction_type', 'amount', 'timestamp', 'description', 'related_account')
