from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing
from .choices import industry_choices, budget_choices, duration_choices
from django.db.models import Q
from companies.models import Company
from django.contrib import messages  # Added import for messages
from applies.models import Apply  # Added import for Apply model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Added import for pagination

# Create your views here.

no_of_job_per_page = 10

def listings(request):
    listings_list = Listing.objects.filter(is_active=True).order_by('-publish_date')
    paginator = Paginator(listings_list, no_of_job_per_page)  
    page = request.GET.get('page')
    
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        listings = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        listings = paginator.page(paginator.num_pages)
    
    context = {
        "listings": listings
    }
    return render(request, 'listings/listings.html', context)

def search(request):
    queryset_list = Listing.objects.filter(is_active=True).order_by('-publish_date')  # Added is_active=True filter
    
    # Get search parameters
    keywords = request.GET.get('keywords', '')
    industry = request.GET.get('industry', '')
    budget = request.GET.get('budget', '')
    duration = request.GET.get('duration', '')
    publish_date = request.GET.get('publish_date', '')
    
    # Apply filters
    if keywords:
        queryset_list = queryset_list.filter(
            Q(title__icontains=keywords)|
            Q(company__name__icontains=keywords)|
            Q(description__icontains=keywords)|
            Q(requirement__icontains=keywords)
        )
    
    if industry:
        queryset_list = queryset_list.filter(
            Q(industry__iexact=industry)
        )
    
    if budget:
        queryset_list = queryset_list.filter(
            Q(budget__iexact=budget)
        )
    
    if duration:
        queryset_list = queryset_list.filter(
            Q(duration__iexact=duration)
        )
    
    if publish_date:
        queryset_list = queryset_list.filter(
            Q(publish_date__gte=publish_date)
        )
    
    # Pagination
    paginator = Paginator(queryset_list, no_of_job_per_page)
    page = request.GET.get('page')
    
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        listings = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        listings = paginator.page(paginator.num_pages)
    
    # Get all GET parameters for preserving search filters in pagination
    get_dict = request.GET.copy()
    if 'page' in get_dict:
        del get_dict['page']
    
    context = {
        "listings": listings,
        "values": request.GET,
        "industry_choices": industry_choices,
        "budget_choices": budget_choices,
        "duration_choices": duration_choices,
        "get_params": get_dict.urlencode() if get_dict else '',  # For preserving search parameters in pagination
    }
    return render(request, 'listings/search.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    company = Company.objects.all()

    # Check if current user is a company HR
    is_company_hr = False
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = Company.objects.get(user=request.user)
            is_company_hr = True
        except Company.DoesNotExist:
            pass

    # Check if current user is the company HR who posted this listing
    is_own_company_listing = False
    if is_company_hr and user_company:
        is_own_company_listing = (listing.company == user_company)

    # Check if user has already applied for this job
    has_applied = False
    existing_application = None
    if request.user.is_authenticated and not is_company_hr:
        try:
            existing_application = Apply.objects.get(listing=listing, user=request.user)
            has_applied = True
        except Apply.DoesNotExist:
            has_applied = False

    # Check if job is inactive and user should have access
    can_view_inactive = False
    if not listing.is_active:
        # Inactive jobs are only visible to:
        # 1. The company HR who posted it
        # 2. Individual users who have applied (and not withdrawn)
        if is_own_company_listing:
            can_view_inactive = True
        elif has_applied:
            can_view_inactive = True
        else:
            # User shouldn't see this inactive job
            messages.error(request, 'This job is no longer available.')
            return redirect('listings:index')

    # Handle POST request for editing job (from modal)
    if request.method == 'POST' and is_own_company_listing:
        # Update the job listing
        listing.title = request.POST.get('title', listing.title)
        listing.industry = request.POST.get('industry', listing.industry)
        listing.budget = request.POST.get('budget', listing.budget)
        listing.duration = request.POST.get('duration', listing.duration)
        listing.requirement = request.POST.get('requirement', listing.requirement)
        listing.description = request.POST.get('description', listing.description)

        # Handle is_active checkbox (returns 'on' when checked, not present when unchecked)
        is_active = request.POST.get('is_active') == 'on'
        listing.is_active = is_active

        listing.save()

        # Add success message
        messages.success(request, 'Job updated successfully!')

        # Redirect back to same page (traditional form submit)
        return redirect('listings:listing', listing_id=listing_id)
    
    context = {
        "listing": listing,
        "company": company,
        "is_company_hr": is_company_hr,
        "is_own_company_listing": is_own_company_listing,
        "has_applied": has_applied,
        "existing_application": existing_application,
        "industry_choices": industry_choices,
        "budget_choices": budget_choices,
        "duration_choices": duration_choices,
    }
    return render(request, 'listings/listing.html', context)

