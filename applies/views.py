from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Apply
from listings.models import Listing

# Create your views here.
@login_required(login_url='accounts:login')
def apply(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Check if user already has an application for this job
    existing_application = None
    try:
        existing_application = Apply.objects.get(listing=listing, user=request.user)
    except Apply.DoesNotExist:
        existing_application = None
    
    if request.method=='POST':
        listing_id = request.POST.get('listing_id')
        name = request.POST.get('name', '')
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '').strip()

        cv_file = request.FILES.get('cv')
        
        if existing_application:
            # Update existing application
            existing_application.name = name
            existing_application.email = email
            existing_application.phone = phone
            existing_application.message = message
            if cv_file:
                existing_application.cv = cv_file
            existing_application.save()
            messages.success(request, 'Application updated successfully')
        else:
            # Create new application
            apply = Apply(listing=listing, listing_id=listing_id, name=name, cv=cv_file,
                            email=email, phone=phone, message=message, user=request.user)
            apply.save()
            messages.success(request, 'Application submitted successfully')
        
        return redirect('accounts:dashboard')
    else:
        # GET request - show form
        if existing_application:
            # Pre-fill form with existing application data
            context = {
                "listing": listing,
                "existing_application": existing_application,
                "is_edit_mode": True
            }
        else:
            # New application - empty form
            context = {
                "listing": listing,
                "existing_application": None,
                "is_edit_mode": False
            }
        return render(request, 'applies/apply.html', context)

@login_required(login_url='accounts:login')
def withdraw_application(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Check if user has an application for this job
    try:
        application = Apply.objects.get(listing=listing, user=request.user)
        
        # Delete the application
        application.delete()
        messages.success(request, 'Your application has been withdrawn successfully.')
        
    except Apply.DoesNotExist:
        messages.error(request, 'You have not applied for this job.')
            
    # Redirect back to the job listing page
    return redirect("accounts:dashboard")
