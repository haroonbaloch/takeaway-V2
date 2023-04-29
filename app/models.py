from django.contrib.auth.models import User
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.gis.db import models as gis_models

from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    operating_hours = models.CharField(max_length=255)
    delivery_areas = models.TextField()
    rating = models.FloatField(default=0)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    location = gis_models.PointField(srid=4326, blank=True, null=True)


    def __str__(self):
        return self.name


class RestaurantDomain(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    domain = models.CharField(max_length=255)

    def __str__(self):
        return self.domain


class Category(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('RECEIVED', 'Received'),
        ('PROCESSING', 'Processing'),
        ('READY', 'Ready'),
        ('DELIVERED', 'Delivered'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RECEIVED')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    pickup_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order {self.id} - {self.restaurant.name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.menu_item.name} x {self.quantity}'

class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.customer.username} for {self.restaurant.name}'

class PromoCode(models.Model):
    code = models.CharField(max_length=255, unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=20)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.code

class Deal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

class Reward(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.points} points'

