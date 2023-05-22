from django.urls import path
from .views import CurrentUserView, CustomTokenObtainPairView, MessageListCreateView, RegisterView, ConnectPartnerView, StatsView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('connectPartner/<str:user_id>/',
         ConnectPartnerView.as_view(), name='connect_parnter'),
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('ourChat/messages/', MessageListCreateView.as_view()),
]
