from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, MarketplaceItem, LostAndFound, RideShare

@login_required
def event_list(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'campus/events.html', {'events': events})

@login_required
def event_create(request):
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST.get('title'),
            event_type=request.POST.get('event_type'),
            description=request.POST.get('description'),
            date=request.POST.get('date'),
            location=request.POST.get('location'),
            organizer=request.POST.get('organizer'),
            posted_by=request.user
        )
        messages.success(request, 'Event added.')
        return redirect('campus:events')
    return render(request, 'campus/event_create.html', {'event_types': Event.EVENT_TYPES})

@login_required
def marketplace(request):
    items = MarketplaceItem.objects.filter(is_sold=False).order_by('-created_at')
    return render(request, 'campus/marketplace.html', {'items': items})

@login_required
def marketplace_create(request):
    if request.method == 'POST':
        MarketplaceItem.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            contact_info=request.POST.get('contact_info'),
            seller=request.user
        )
        messages.success(request, 'Item listed on marketplace.')
        return redirect('campus:marketplace')
    return render(request, 'campus/marketplace_create.html')

@login_required
def lost_found_list(request):
    items = LostAndFound.objects.filter(is_resolved=False).order_by('-created_at')
    return render(request, 'campus/lost_found.html', {'items': items})

@login_required
def lost_found_create(request):
    if request.method == 'POST':
        LostAndFound.objects.create(
            item_type=request.POST.get('item_type'),
            item_name=request.POST.get('item_name'),
            description=request.POST.get('description'),
            date_lost_found=request.POST.get('date_lost_found'),
            contact_info=request.POST.get('contact_info'),
            posted_by=request.user
        )
        messages.success(request, 'Lost/Found item reported.')
        return redirect('campus:lost_found')
    return render(request, 'campus/lost_found_create.html', {'item_types': LostAndFound.ITEM_TYPES})

@login_required
def rideshare_list(request):
    rides = RideShare.objects.filter(departure_time__gte=timezone.now()).order_by('departure_time')
    return render(request, 'campus/rideshare.html', {'rides': rides})

@login_required
def rideshare_create(request):
    if request.method == 'POST':
        seats = request.POST.get('available_seats')
        RideShare.objects.create(
            ride_type=request.POST.get('ride_type'),
            source=request.POST.get('source'),
            destination=request.POST.get('destination'),
            departure_time=request.POST.get('departure_time'),
            available_seats=seats if seats else None,
            contact_info=request.POST.get('contact_info'),
            posted_by=request.user
        )
        messages.success(request, 'Ride share posted.')
        return redirect('campus:rides')
    return render(request, 'campus/rideshare_create.html', {'ride_types': RideShare.RIDE_TYPES})
