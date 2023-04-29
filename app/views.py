

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework.decorators import action

from rest_framework.views import APIView

from takeaway import settings
from .models import Category, MenuItem, Order, OrderItem, Review, Deal, Reward, Restaurant
from .serializers import (CategorySerializer, MenuItemSerializer,
                          OrderSerializer, OrderItemSerializer, ReviewSerializer, DealSerializer, RewardSerializer,
                          RestaurantSerializer)



class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["get"])
    def menu_items(self, request, pk=None):
        menu_items = MenuItem.objects.filter(restaurant_id=pk)
        serialized_menu_items = [MenuItemSerializer(menu_item).data for menu_item in menu_items]
        return Response(serialized_menu_items)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [AllowAny]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # Custom logic to handle order creation, such as calculating total
        menu_items = request.data['menu_items']
        total = 0
        for item in menu_items:
            menu_item = MenuItem.objects.get(id=item['id'])
            total += menu_item.price * item['quantity']
        request.data['total'] = total
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        status = request.data['status']
        if status in ['PROCESSING', 'READY', 'DELIVERED']:
            order.status = status
            order.save()
            return Response({'status': status})
        else:
            return Response({'status': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

import json
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def charge(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_method_id = data.get('paymentMethodId')
            amount = data.get('amount')

            payment_intent = stripe.PaymentIntent.create(
                payment_method=payment_method_id,
                amount=int(amount * 100),  # Convert to cents
                currency='gbp',
                confirmation_method='manual',
                confirm=True,
            )

            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
# class RestaurantMenuItemsView(APIView):
#     def get(self, request, restaurant_id):
#         menu_items = MenuItem.objects.filter(restaurant_id=restaurant_id)
#         serialized_menu_items = [MenuItemSerializer(menu_item).data for menu_item in menu_items]
#         return Response(serialized_menu_items)

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

def get_nearby_restaurants(request):
    lat = float(request.GET.get('lat'))
    lng = float(request.GET.get('lng'))
    radius = float(request.GET.get('radius')) * 1000  # Convert to meters

    user_location = Point(lng, lat, srid=4326)
    queryset = Restaurant.objects.annotate(distance=Distance('location', user_location)).filter(distance__lte=radius)
