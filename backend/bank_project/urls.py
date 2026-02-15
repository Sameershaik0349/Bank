from django.contrib import admin
from django.urls import path, include
from bank_project.admin_views import custom_admin_login_view
from accounts.admin_forms import CustomAdminLoginForm

# Configure Custom Admin Login Form
admin.site.login_form = CustomAdminLoginForm

urlpatterns = [
    # Intercept admin login to enforce logout for non-staff users
    path('admin/login/', custom_admin_login_view),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('banking/', include('banking.urls')),
    path('api/', include('api.urls')),
    path('', include('banking.urls')),   # dashboard as home
]
