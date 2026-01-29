from django.urls import path
from .views import ProfileDetailView, BusinessProfileListView, CustomerProfileListView

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profiles/business/", BusinessProfileListView.as_view(), name="profiles-business"),
    path("profiles/customer/", CustomerProfileListView.as_view(), name="profiles-customer"),
]
