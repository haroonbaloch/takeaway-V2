from django.contrib.auth.models import User
from app.models import Restaurant, RestaurantDomain

def create_restaurant():
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

if __name__ == '__main__':
    create_restaurant()
