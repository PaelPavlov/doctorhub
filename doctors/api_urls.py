from rest_framework.routers import DefaultRouter
from .views import DoctorProfileViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorProfileViewSet, basename='doctor')

urlpatterns = router.urls