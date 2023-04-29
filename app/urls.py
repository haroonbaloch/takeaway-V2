from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from takeaway import settings
from . import views


router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'menu-items', views.MenuItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'deals', views.DealViewSet)
router.register(r'rewards', views.RewardViewSet)
router.register(r'restaurants', views.RestaurantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('charge/', views.charge, name='charge'),

    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # path('restaurants/<int:restaurant_id>/menu-items/', RestaurantMenuItemsView.as_view()),  # Add this line
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
