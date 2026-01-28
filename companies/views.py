from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from .models import Company
from listings.models import Listing
from applies.models import Apply
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from listings.choices import industry_choices, budget_choices, duration_choices
from django.db.models import Count, Q  # Added Count and Q for aggregation

# Create your views here.
def company(request,company_id):
    company = get_object_or_404(Company, pk = company_id)
    
    # Check if the current user is the HR (owner) of this company
    is_company_hr = request.user.is_authenticated and hasattr(request.user, 'company') and request.user.company.id == company.id
    
    # Get job listings based on user type
    if is_company_hr:
        # Company HR sees ALL jobs (active and inactive)
        job_listings = Listing.objects.filter(company=company).order_by('-publish_date')
    else:
        # Regular users see only ACTIVE jobs
        job_listings = Listing.objects.filter(company=company, is_active=True).order_by('-publish_date')
    
    context = {
        'company': company,
        'job_listings': job_listings,
        'is_company_hr': is_company_hr
    }
    return render(request,'companies/company.html', context)

@login_required
def HR_dashboard(request):
    # Check if user is associated with a company
    try:
        company = Company.objects.get(user=request.user)

        # Get job posts with applicant count annotation
        job_posts = Listing.objects.filter(company=company).annotate(
            applicant_count=Count('applications')
        ).order_by('-publish_date')
        
        # Calculate statistics
        total_jobs = job_posts.count()
        active_jobs = job_posts.filter(is_active=True).count()
        
        # Calculate total applicants across all jobs
        total_applicants = 0
        for job in job_posts:
            total_applicants += job.applicant_count
        
        # Check if company info is complete
        # Essential fields: name, email, phone, industry, description
        company_info_complete = all([
            company.name,
            company.email,
            company.phone and company.phone != '00000000',
            company.industry,
            company.description
        ])
        
        context = {
            "company": company,
            "job_post": job_posts,
            "company_info_complete": company_info_complete,
            "total_jobs": total_jobs,
            "active_jobs": active_jobs,
            "total_applicants": total_applicants,
        }
        return render(request, 'companies/HR_dashboard.html', context)
    except Company.DoesNotExist:
        # User is not a company HR, silently redirect to individual dashboard
        return redirect('accounts:dashboard')

@login_required
def company_edit_info(request):
    # Check if user is associated with a company
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        # User is not a company HR, silently redirect to individual dashboard
        return redirect('accounts:dashboard')
    

    if request.method=='POST':
        user_id = request.POST['user_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        industry = request.POST.get('industry', '')
        serivces = request.POST.get('serivces', '')
        description = request.POST['description']
        
        # Update company info
        company.name = name
        company.email = email
        company.phone = phone
        company.industry = industry
        company.serivces = serivces
        company.description = description

        # Handle logo file upload
        if 'logo' in request.FILES:
            company.logo = request.FILES['logo']

        company.save()
        
        messages.success(request, 'Company information updated successfully')
        return redirect('companies:HR_dashboard')  
    else:
        # Import industry choices from listings
        from listings.choices import industry_choices
        context = {
            "company": company,
            "industry_choices": industry_choices
    }
        return render(request, 'companies/company_edit_info.html', context)

@login_required
def job_post(request):
    # Check if user is associated with a company
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        # User is not a company HR, silently redirect to individual dashboard
        return redirect('accounts:dashboard')
    
    if request.method=='POST':
        title = request.POST['title']
        industry = request.POST['industry']
        budget = request.POST['budget']
        duration = request.POST['duration']
        requirement = request.POST['requirement']
        description = request.POST['description']
        
        listing = Listing.objects.create(
            title=title, 
            company=company,
            industry=industry,
            budget=budget,
            duration=duration,
            requirement=requirement, 
            description=description
        )
        listing.save()
        
        messages.success(request, 'Job posted successfully')
        return redirect('companies:HR_dashboard')
    else:
        context = {
            "company": company,
            "industry_choices": industry_choices,
            "budget_choices": budget_choices,
            "duration_choices": duration_choices
    }
        return render(request,'companies/job_post.html', context)
    
@login_required
def view_candidate(request, listing_id):
    # Check if user is associated with a company
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        # User is not a company HR, silently redirect to individual dashboard
        return redirect('accounts:dashboard')
    
    # Verify that the listing belongs to the user's company
    listing = get_object_or_404(Listing, pk=listing_id, company=company)
    
    user_appliers = Apply.objects.all().filter(
        listing_id = listing_id).order_by('-apply_date')
    context = {
        "listing": listing,
        "user_appliers": user_appliers
    }
    return render(request, 'companies/view_candidate.html', context)

@login_required
def toggle_job_status(request, listing_id):
    # Check if user is associated with a company
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        # User is not a company HR
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('accounts:dashboard')
    
    # Verify that the listing belongs to the user's company
    listing = get_object_or_404(Listing, pk=listing_id, company=company)
    
    # Toggle the is_active status
    listing.is_active = not listing.is_active
    listing.save()
    
    # Set appropriate message
    if listing.is_active:
        messages.success(request, f'Job "{listing.title}" has been activated and is now visible to candidates.')
    else:
        messages.success(request, f'Job "{listing.title}" has been deactivated and is now hidden from candidates.')
    
    # Redirect back to HR dashboard
    return redirect('companies:HR_dashboard')
