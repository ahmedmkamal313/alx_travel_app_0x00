from django.db import models
from django.utils import timezone


class Listing(models.Model):
    """
    Represents a property listing available for booking.
    """
    title = models.CharField(max_length=255, help_text="Title of the listing")
    description = models.TextField(
        help_text="Detailed description of the listing")
    address = models.CharField(
        max_length=255, help_text="Physical address of the property")
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price per night in USD")
    max_guests = models.IntegerField(
        help_text="Maximum number of guests allowed")
    bedrooms = models.IntegerField(help_text="Number of bedrooms")
    bathrooms = models.DecimalField(
        max_digits=3, decimal_places=1, help_text="Number of bathrooms (e.g., 2.5)")
    is_published = models.BooleanField(
        default=True, help_text="Is the listing currently published?")
    created_at = models.DateTimeField(
        default=timezone.now, help_text="Timestamp when the listing was created")
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the listing was last updated")

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"
        # Order listings by creation date, newest first
        ordering = ['-created_at']

    def __str__(self):
        """String representation of the Listing."""
        return self.title


class Booking(models.Model):
    """
    Represents a booking made by a guest for a specific listing.
    """
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,  # If a listing is deleted, its bookings are also deleted
        # Allows accessing bookings from a Listing instance (e.g., listing.bookings.all())
        related_name='bookings',
        help_text="The listing being booked"
    )
    guest_name = models.CharField(
        max_length=255, help_text="Name of the guest making the booking")
    guest_email = models.EmailField(
        help_text="Email of the guest making the booking")
    check_in_date = models.DateField(help_text="Date of check-in")
    check_out_date = models.DateField(help_text="Date of check-out")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Total price for the booking")
    created_at = models.DateTimeField(
        default=timezone.now, help_text="Timestamp when the booking was created")

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        # Ensure that a guest cannot book the same listing for overlapping dates
        # This would typically be handled at the application level during booking creation,
        # but a unique_together constraint can add a layer of database-level protection
        # if combined with a check for non-overlapping dates in the application logic.
        # For simplicity of this model, we'll just ensure unique guest+listing+check_in combination.
        # A more robust solution for overlapping dates requires custom validation.
        unique_together = ('listing', 'guest_email', 'check_in_date')
        ordering = ['check_in_date']  # Order bookings by check-in date

    def __str__(self):
        """String representation of the Booking."""
        return f"Booking for {self.listing.title} by {self.guest_name} from {self.check_in_date} to {self.check_out_date}"


class Review(models.Model):
    """
    Represents a review given by a guest for a listing.
    """
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,  # If a listing is deleted, its reviews are also deleted
        # Allows accessing reviews from a Listing instance (e.g., listing.reviews.all())
        related_name='reviews',
        help_text="The listing being reviewed"
    )
    guest_name = models.CharField(
        max_length=255, help_text="Name of the guest who wrote the review")
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],  # Rating from 1 to 5
        help_text="Rating given by the guest (1-5)"
    )
    comment = models.TextField(
        blank=True, null=True, help_text="Optional comment from the guest")
    created_at = models.DateTimeField(
        default=timezone.now, help_text="Timestamp when the review was created")

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        # Ensure a guest can only review a specific listing once
        unique_together = ('listing', 'guest_name')
        # Order reviews by creation date, newest first
        ordering = ['-created_at']

    def __str__(self):
        """String representation of the Review."""
        return f"Review for {self.listing.title} by {self.guest_name} - Rating: {self.rating}"
