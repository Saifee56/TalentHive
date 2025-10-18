from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .applicant_profile_viewset import ApplicantProfileViewset

# from .interview_viewset --->pending

app_name='applicant'

router = DefaultRouter()
router.register('applicant-profile',ApplicantProfileViewset,basename='applicant-profile')


urlpatterns = [
    path('', include(router.urls)),
]