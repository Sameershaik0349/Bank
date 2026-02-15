from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
from django.contrib import messages
from django.db import transaction
from decimal import Decimal

def landing(request):
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    accounts = BankAccount.objects.filter(user=request.user)
    recent_transactions = Transaction.objects.filter(account__user=request.user).order_by('-timestamp')[:10]
    return render(request, 'banking/dashboard.html', {
        'accounts': accounts,
        'recent_transactions': recent_transactions
    })

@login_required
def create_account(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        initial_deposit = Decimal(request.POST.get('initial_deposit', '0'))

        if initial_deposit < 100:
            messages.error(request, "Minimum initial deposit is ₹100.")
            return render(request, 'banking/create_account.html')

        if account_type in ['SAVINGS', 'CURRENT']:
            with transaction.atomic():
                account = BankAccount.objects.create(
                    user=request.user, 
                    account_type=account_type,
                    balance=initial_deposit
                )
                
                # Record Initial Deposit Transaction
                Transaction.objects.create(
                    account=account,
                    transaction_type='DEPOSIT',
                    amount=initial_deposit,
                    description='Initial Deposit'
                )

            messages.success(request, f"<strong>Account Created Successfully</strong><br>Your {account_type.lower()} account has been created with an initial deposit of ₹{initial_deposit}.")
            return redirect('dashboard')
            
    return render(request, 'banking/create_account.html')

@login_required
def deposit(request):
    accounts = BankAccount.objects.filter(user=request.user)
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        amount = Decimal(request.POST.get('amount'))
        
        if amount <= 0:
            messages.error(request, "Amount must be positive.")
        else:
            with transaction.atomic():
                account = BankAccount.objects.get(id=account_id, user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    transaction_type='DEPOSIT',
                    amount=amount,
                    description=f"Deposit to {account.account_number}"
                )
            messages.success(request, f"<strong>Deposit Successful</strong><br>₹{amount} has been successfully added to your account.")

            return redirect('dashboard')
            
    return render(request, 'banking/deposit.html', {'accounts': accounts})

@login_required
def withdraw(request):
    accounts = BankAccount.objects.filter(user=request.user)
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        amount = Decimal(request.POST.get('amount'))
        
        account = BankAccount.objects.get(id=account_id, user=request.user)
        if amount <= 0:
            messages.error(request, "Amount must be positive.")
        elif account.balance < amount:
            messages.error(request, "Insufficient funds.")
        else:
            with transaction.atomic():
                account.balance -= amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    transaction_type='WITHDRAWAL',
                    amount=amount,
                    description=f"Withdrawal from {account.account_number}"
                )
            messages.success(request, f"<strong>Withdrawal Successful</strong><br>₹{amount} has been successfully withdrawn from your account.")

            return redirect('dashboard')
            
    return render(request, 'banking/withdraw.html', {'accounts': accounts})

@login_required
def transfer(request):
    my_accounts = BankAccount.objects.filter(user=request.user)
    if request.method == 'POST':
        from_account_id = request.POST.get('from_account_id')
        to_account_number = request.POST.get('to_account_number')
        amount = Decimal(request.POST.get('amount'))
        
        try:
            from_account = BankAccount.objects.get(id=from_account_id, user=request.user)
            to_account = BankAccount.objects.get(account_number=to_account_number)
            
            if from_account == to_account:
                messages.error(request, "Cannot transfer to the same account.")
            elif amount <= 0:
                messages.error(request, "Amount must be positive.")
            elif from_account.balance < amount:
                messages.error(request, "Insufficient funds.")
            else:
                with transaction.atomic():
                    # Deduct from source
                    from_account.balance -= amount
                    from_account.save()
                    
                    # Add to destination
                    to_account.balance += amount
                    to_account.save()
                    
                    # Record transactions for both
                    Transaction.objects.create(
                        account=from_account,
                        transaction_type='TRANSFER',
                        amount=amount,
                        description=f"Transfer to {to_account.account_number}",
                        related_account=to_account
                    )
                    Transaction.objects.create(
                        account=to_account,
                        transaction_type='DEPOSIT', # From the perspective of receiver
                        amount=amount,
                        description=f"Transfer from {from_account.account_number}",
                        related_account=from_account
                    )
                messages.success(request, f"<strong>Transfer Successful</strong><br>₹{amount} has been successfully transferred to {to_account_number}.")

                return redirect('dashboard')
        except BankAccount.DoesNotExist:
            messages.error(request, "Destination account not found.")
            
    return render(request, 'banking/transfer.html', {'accounts': my_accounts})
