from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Apps
    path('product/', include('product.urls')),
    path('category/', include('category.urls')),
    path('customer/', include('customer.urls')),
    path('staff/', include('staff.urls')),
    path('subscription/', include('subscription.urls')),
    path('order/', include('order.urls')),
]