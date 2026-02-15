from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

def csrf_failure(request, reason=""):
    """
    Custom CSRF failure handler.
    Redirects user to login page with a friendly error message instead of showing 403 Forbidden.
    """
    # Determine where to redirect based on the request path
    if request.path.startswith('/admin/'):
        redirect_url = 'admin:login'
    else:
        redirect_url = 'login'
    
    # Add a user-friendly error message
    messages.error(request, "Session expired or invalid. Please login again.")
    
    # Redirect to the appropriate login page
    try:
        return redirect(redirect_url)
    except:
        # Fallback if reverse lookup fails
        return redirect('/admin/login/' if request.path.startswith('/admin/') else '/login/')
