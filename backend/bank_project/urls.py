from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from bank_project.admin_views import custom_admin_login_view
from accounts.admin_forms import CustomAdminLoginForm

# Configure Custom Admin Login Form
admin.site.login_form = CustomAdminLoginForm

urlpatterns = [
    # Favicon
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('favicon.ico')
    )),

    # Custom Admin Login
    path('admin/login/', custom_admin_login_view),
    path('admin/', admin.site.urls),

    # Auth & Apps
    path('accounts/', include('accounts.urls')),
    path('banking/', include('banking.urls')),
    path('api/', include('api.urls')),

    # MAIN OPENING PAGE (HOME / LANDING)
    path('', include('banking.urls')),   # home / landing
]
