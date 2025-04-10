# vendor/middleware.py
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse, NoReverseMatch

class VendorApprovalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = []

        # Safely initialize exempt paths
        try:
            self.exempt_paths = [
                reverse('userauths:sign-in'),
                reverse('userauths:sign-up'),
                reverse('userauths:sign-out'),  # Changed from 'logout' to match your URL name
                '/admin/',
                '/vendor/approval-pending/',
            ]
        except NoReverseMatch as e:
            # Fallback paths if reverse fails
            self.exempt_paths = [
                '/auth/sign-in/',
                '/auth/sign-up/',
                '/auth/sign-out/',
                '/admin/',
                '/vendor/approval-pending/',
            ]

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip middleware for exempt paths
        if any(request.path.startswith(path) for path in self.exempt_paths):
            return None
        
        # Check only authenticated users with vendor profile
        if request.user.is_authenticated and hasattr(request.user, 'vendor'):
            vendor = request.user.vendor
            
            # Vendor not approved
            if not vendor.is_approved:
                # If trying to access vendor-specific pages
                if request.path.startswith('/vendor/') and not request.path.startswith('/vendor/approval-pending/'):
                    messages.warning(request, "Your vendor account is pending approval.")
                    return redirect('vendor:approval-pending')
                return None
            
            # Vendor deactivated
            if not vendor.is_active:
                messages.error(request, "Your vendor account has been deactivated.")
                return redirect('userauths:sign-in')
        
        return None
    
    
