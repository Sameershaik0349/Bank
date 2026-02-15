from django.db import models
from django.conf import settings
import uuid


class BankAccount(models.Model):
    ACCOUNT_TYPES = (
        ('SAVINGS', 'Savings'),
        ('CURRENT', 'Current'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    account_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True
    )
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPES,
        default='SAVINGS'
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = str(uuid.uuid4().hex)[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.account_number} ({self.account_type})"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    )

    account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    related_account = models.ForeignKey(
        BankAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incoming_transfers'
    )
    transaction_type = models.CharField(
        max_length=15,
        choices=TRANSACTION_TYPES
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.account.account_number}"
