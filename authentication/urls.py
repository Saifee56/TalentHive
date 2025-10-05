from rest_framework import routers
from .auth_viewset import AuthenticationViewSet

app_name='authentication'

router=routers.DefaultRouter()
router.register(r'auth',AuthenticationViewSet,basename='auth')

urlpatterns = router.urls