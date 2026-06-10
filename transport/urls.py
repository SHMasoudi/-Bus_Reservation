from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransportCompanyViewSet, BusViewSet, SeatViewSet, TripViewSet

router = DefaultRouter()
router.register('companies', TransportCompanyViewSet, basename='company')
router.register('buses', BusViewSet, basename='bus')
router.register('seats', SeatViewSet, basename='seat')
router.register('trips', TripViewSet, basename='trip')

urlpatterns = [
    path('', include(router.urls)),
]


"""
GET  /companies/        → لیست همه شرکت‌ها
POST /companies/        → ساخت شرکت جدید
GET  /companies/1/      → جزئیات شرکت ۱
PUT  /companies/1/      → ویرایش شرکت ۱
DELETE /companies/1/    → حذف شرکت ۱

"""
