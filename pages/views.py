from django.shortcuts import render
from listings.models import Listing
from listings.choices import industry_choices, budget_choices, duration_choices

def index(request):
    listings = Listing.objects.order_by('-publish_date').filter(is_active=True)[:3]
    context = {
        'listings': listings,
        'industry_choices': industry_choices,
        'budget_choices': budget_choices,
        'duration_choices': duration_choices,
        'values': request.GET,
    }
    return render(request,'pages/index.html', context)

def about (request):
    return render(request,'pages/about.html')
