from django.db import models
from accounts.models import User

class Event(models.Model):
    EVENT_TYPES = [
        ('society', 'Society Event'),
        ('hostel', 'Hostel Event'),
        ('sports', 'Sports Meet'),
        ('seminar', 'Seminar'),
    ]
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.CharField(max_length=100) # Society name or individual
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class MarketplaceItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contact_info = models.CharField(max_length=200, help_text="Phone number or WhatsApp link")
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class LostAndFound(models.Model):
    ITEM_TYPES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    item_name = models.CharField(max_length=200)
    description = models.TextField(help_text="Provide details like color, brand, location.")
    date_lost_found = models.DateField()
    contact_info = models.CharField(max_length=200)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_item_type_display()}: {self.item_name}"

class RideShare(models.Model):
    RIDE_TYPES = [
        ('offering', 'Offering a Ride'),
        ('seeking', 'Seeking a Ride'),
    ]
    ride_type = models.CharField(max_length=10, choices=RIDE_TYPES)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField(null=True, blank=True)
    contact_info = models.CharField(max_length=200)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_ride_type_display()} from {self.source} to {self.destination}"
