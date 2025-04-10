# userauths/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from userauths import models as userauths_models
from userauths import forms as userauths_forms
from vendor import models as vendor_models
from .utils import check_role_customer, check_role_vendor, redirect_by_user_type, customer_required, vendor_required

from django.core.mail import send_mail
from django.conf import settings

def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect(redirect_by_user_type(request.user))

    form = userauths_forms.UserRegisterForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        try:
            user = form.save()
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            mobile = form.cleaned_data.get('mobile')
            password = form.cleaned_data.get('password1')
            user_type = form.cleaned_data.get("user_type")
            vendor_license = form.cleaned_data.get("vendor_license")

            profile = userauths_models.Profile.objects.create(
                full_name=full_name, 
                mobile=mobile, 
                user=user,
                user_type=user_type,
                vendor_license=vendor_license if user_type == "Vendor" else None
            )
            
            if user_type == "Vendor":
                vendor = vendor_models.Vendor.objects.create(
                    user=user, 
                    store_name=full_name, 
                    is_approved=False
                )
                
                # Get site URL safely
                site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
                
                # Notify admin
                try:
                    admin_subject = f"New Vendor Approval Request: {full_name}"
                    admin_message = f"""
                    A new vendor {full_name} has registered and is awaiting approval.
                    
                    License: {vendor_license}
                    
                    Review: {site_url}/admin/vendor/vendor/{vendor.id}/change/
                    """
                    
                    send_mail(
                        admin_subject,
                        admin_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.ADMIN_EMAIL],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Failed to send admin email: {e}")

                # Notify vendor
                try:
                    vendor_subject = "Vendor Account Pending Approval"
                    vendor_message = "Thank you for registering as a vendor. Your account is pending admin approval."
                    send_mail(
                        vendor_subject,
                        vendor_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Failed to send vendor email: {e}")

                messages.info(request, "Your vendor account is pending admin approval.")
                return redirect('userauths:sign-in')
            else:
                # Regular user flow
                user = authenticate(email=email, password=password)
                login(request, user)
                messages.success(request, "Account created successfully!")
                return redirect(redirect_by_user_type(user))
        
        except Exception as e:
            messages.error(request, f"An error occurred during registration: {str(e)}")
            return redirect('userauths:sign-up')
    
    context = {'form': form}
    return render(request, 'userauths/sign-up.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect(redirect_by_user_type(request.user))
    
    if request.method == 'POST':
        form = userauths_forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                # Vendor approval check
                if hasattr(user, 'vendor'):
                    if not user.vendor.is_approved:
                        messages.warning(request, "Your vendor account is pending admin approval.")
                        return redirect('userauths:sign-in')
                    
                    if not user.vendor.is_active:
                        messages.error(request, "Your vendor account has been deactivated.")
                        return redirect('userauths:sign-in')
                
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect(redirect_by_user_type(user))
            else:
                messages.error(request, 'Invalid email or password')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return render(request, "userauths/sign-in.html", {'form': userauths_forms.LoginForm()})

def logout_view(request):
    if "cart_id" in request.session:
        cart_id = request.session['cart_id']
    else:
        cart_id = None
    logout(request)
    request.session['cart_id'] = cart_id
    messages.success(request, 'You have been logged out.')
    return redirect("userauths:sign-in")

# Example protected views
@vendor_required
def vendor_dashboard(request):
    return render(request, 'vendor/dashboard.html')

@customer_required
def customer_dashboard(request):
    return render(request, 'customer/dashboard.html')

def handler404(request, exception, *args, **kwargs):
    return render(request, 'userauths/404.html', status=404)

def handler500(request, *args, **kwargs):
    return render(request, 'userauths/500.html', status=500)