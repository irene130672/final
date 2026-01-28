from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from applies.models import Apply
from companies.models import Company
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

def register(request):
    if request.method == 'POST':
        # Handle registration logic here
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        # Get account_type and company_name with defaults
        account_type = request.POST.get('account_type', 'user')
        company_name = request.POST.get('company_name', '')
        phone = request.POST.get('phone', '00000000')  # Get phone with default

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect("accounts:register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect("accounts:register")
                else:
                    # Create user
                    user = User.objects.create_user(
                        username=username, 
                        password=password, 
                        email=email, 
                        first_name=first_name, 
                        last_name=last_name
                    )
                    user.save()

                    # If account type is company, create Company record
                    if account_type == 'company' and company_name:
                        company = Company.objects.create(
                            name=company_name,
                            email=email,
                            phone=phone,  # Save phone from registration
                            user=user,
                            serivces=''  # Initialize with empty services
                        )
                        company.save()
                        messages.success(request, 'Company HR account created successfully')
                    else:
                        messages.success(request, 'You are now registered and can log in')
                    
                    return redirect("accounts:login")
        else:
            messages.error(request, 'Passwords do not match')
            return redirect("accounts:register")
    else:    
        # Get account_type from URL parameter
        url_account_type = request.GET.get('account_type', 'user')

        # Map URL parameters to form values
        account_type_map = {
            'individual': 'user',
            'hr': 'company',
            'user': 'user',
            'company': 'company'
        }

        # Get the mapped account type, default to 'user'
        account_type = account_type_map.get(url_account_type, 'user')

        context = {
            'account_type': account_type
        }
        return render(request, 'accounts/register.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            
            # Check if user is associated with a company
            try:
                company = Company.objects.get(user=user)
                # User is a company HR, redirect to HR dashboard
                return redirect('companies:HR_dashboard')
            except Company.DoesNotExist:
                # User is an individual, redirect to regular dashboard
                return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')
    return render(request, "accounts/login.html")

def logout_view(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('pages:index')

@login_required
def dashboard(request):
    # Check if user is a company HR, redirect if they are
    try:
        company = Company.objects.get(user=request.user)
        # User is a company HR, silently redirect to HR dashboard
        return redirect('companies:HR_dashboard')
    except Company.DoesNotExist:
        # User is an individual, show their dashboard
        apply = Apply.objects.filter(user=request.user).order_by('-apply_date')
        context = {'apply': apply}
        return render(request, "accounts/dashboard.html", context)

def custom_password_reset(request):
    """Custom password reset view with debug logging"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        print(f"DEBUG: Password reset requested for email: '{email}'")

        # Check if user exists
        users = User.objects.filter(email__iexact=email)
        print(f"DEBUG: Found {users.count()} user(s) with email '{email}'")

        for user in users:
            print(f"DEBUG: User found - username: {user.username}, email: {user.email}, is_active: {user.is_active}")
            # Check if user is associated with a company
            try:
                company = Company.objects.get(user=user)
                print(f"DEBUG: User is a company HR for company: {company.name}")
            except Company.DoesNotExist:
                print(f"DEBUG: User is an individual user")

    # Use Django's built-in PasswordResetView
    return PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        success_url=reverse_lazy('accounts:password_reset_done'),
        email_template_name="registration/password_reset_email.html"
    )(request)

