from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.
    Converts Listing model instances to JSON and vice-versa.
    """
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'address', 'price_per_night',
            'max_guests', 'bedrooms', 'bathrooms', 'is_published',
            'created_at', 'updated_at'
        ]
        # These fields are set automatically
        read_only_fields = ['created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    Converts Booking model instances to JSON and vice-versa.
    """
    # Display the listing's title instead of just its ID
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'guest_name', 'guest_email',
            'check_in_date', 'check_out_date', 'total_price', 'created_at'
        ]
        # total_price computed, created_at set automatically
        read_only_fields = ['total_price', 'created_at']

    def validate(self, data):
        """
        Custom validation for Booking dates.
        Ensures check_out_date is not before check_in_date.
        """
        if data['check_in_date'] >= data['check_out_date']:
            raise serializers.ValidationError(
                {"check_out_date": "Check-out date must be after check-in date."}
            )
        return dat
