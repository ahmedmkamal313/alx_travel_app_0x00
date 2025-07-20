import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seeds the database with sample data for Listings, Bookings, and Reviews.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_listings',
            type=int,
            default=10,
            help='The number of sample listings to create.'
        )
        parser.add_argument(
            '--clear_existing',
            action='store_true',
            help='Clear all existing data before seeding.'
        )

    def handle(self, *args, **options):
        fake = Faker()
        num_listings = options['num_listings']
        clear_existing = options['clear_existing']

        if clear_existing:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        self.stdout.write(self.style.MIGRATE_HEADING(
            f'Seeding {num_listings} listings...'))

        for i in range(num_listings):
            # Create Listing
            listing = Listing.objects.create(
                title=fake.sentence(nb_words=random.randint(3, 7)),
                description=fake.paragraph(nb_sentences=random.randint(3, 8)),
                address=fake.address(),
                price_per_night=random.uniform(50.00, 500.00),
                max_guests=random.randint(1, 10),
                bedrooms=random.randint(1, 5),
                bathrooms=random.choice([1.0, 1.5, 2.0, 2.5, 3.0]),
                is_published=fake.boolean(chance_of_getting_true=90),
                created_at=timezone.now() - timedelta(days=random.randint(1, 365))
            )
            self.stdout.write(f'Created Listing: "{listing.title}"')

            # Create 0-5 Bookings for each Listing
            num_bookings = random.randint(0, 5)
            for _ in range(num_bookings):
                check_in = timezone.now().date() + timedelta(days=random.randint(1, 60))
                check_out = check_in + timedelta(days=random.randint(1, 14))
                total_price = listing.price_per_night * \
                    (check_out - check_in).days

                # Ensure total_price is positive (at least 1 night)
                if total_price <= 0:
                    total_price = listing.price_per_night  # Fallback for 0-day bookings

                Booking.objects.create(
                    listing=listing,
                    guest_name=fake.name(),
                    guest_email=fake.email(),
                    check_in_date=check_in,
                    check_out_date=check_out,
                    total_price=total_price,
                    created_at=timezone.now() - timedelta(days=random.randint(0, 30))
                )

            # Create 0-10 Reviews for each Listing
            num_reviews = random.randint(0, 10)
            for _ in range(num_reviews):
                Review.objects.create(
                    listing=listing,
                    guest_name=fake.name(),
                    rating=random.randint(1, 5),
                    comment=fake.paragraph(nb_sentences=random.randint(
                        1, 3)) if fake.boolean(chance_of_getting_true=70) else None,
                    created_at=timezone.now() - timedelta(days=random.randint(0, 60))
                )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {num_listings} listings with associated bookings and reviews.'))
