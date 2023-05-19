from django.urls import path
from .views import CurrentUserView, MessageListCreateView, PartnerDetailView, RegisterView, ConnectPartnerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('connectPartner/<str:user_id>/',
         ConnectPartnerView.as_view(), name='connect_parnter'),
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('partner/', PartnerDetailView.as_view(), name='partner_detail'),
    path('ourChat/messages/', MessageListCreateView.as_view()),
]
