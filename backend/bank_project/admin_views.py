from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.admin import site
from accounts.admin_forms import CustomAdminLoginForm

def custom_admin_login_view(request):
    """
    Custom view for Admin Login.
    Ensures that non-staff users are logged out before accessing the admin login page
    to prevent session confusion and auto-fill issues.
    """
    if request.user.is_authenticated and not request.user.is_staff:
        logout(request)
        messages.warning(request, "Please login with an admin account.")
        return redirect('admin:login')
    
    # Use the default admin site login but with our custom form and context
    # We set the login form here dynamically for this request context if needed, 
    # but strictly setting it in urls.py or admin.site is better.
    # However, since we are wrapping the view, we can just call it.
    
    # Actually, to use the custom form with the standard admin login view, 
    # we should configure admin.site.login_form in urls.py.
    # This view is mainly to intercept the request for logout logic.
    
    return site.login(request)
