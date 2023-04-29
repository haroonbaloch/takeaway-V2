from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from app.models import Restaurant, RestaurantDomain

class Command(BaseCommand):
    help = 'Creates a new restaurant'

    def handle(self, *args, **options):
        # create your public tenant
        restaurant = Restaurant(schema_name='restaurant1',
                                name='My First Restaurant',
                                owner=User.objects.first())
        restaurant.save()

        # Add one or more domains for the tenant
        domain = RestaurantDomain()
        domain.domain = 'restaurant1.my-domain.com'
        domain.tenant = restaurant
        domain.is_primary = True
        domain.save()

        self.stdout.write(self.style.SUCCESS('Restaurant created successfully.'))
