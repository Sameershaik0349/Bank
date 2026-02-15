from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('dashboard')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if not password:
             messages.error(request, "Password is required to delete your account.")
             return redirect('profile')
        
        if not request.user.check_password(password):
            messages.error(request, "Incorrect password. Account deletion failed.")
            return redirect('profile')
        
        # Determine if user is actually user or admin
        if request.user.is_superuser or request.user.is_staff:
             messages.error(request, "Admin accounts cannot be deleted via this interface.")
             return redirect('profile')

        user = request.user
        logout(request) # Log out before deleting
        user.delete()
        messages.success(request, "Your account has been permanently deleted.")
        return redirect('login')
    
    return redirect('profile')
