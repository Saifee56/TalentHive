from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .recruiter_profile_viewset import RecruiterProfileViewset
from .job_post_viewset import JobPostViewset
# from .interview_viewset --->pending

app_name='recruiter'

router = DefaultRouter()
router.register('recruiter-profile',RecruiterProfileViewset,basename='recruiter-profile')
router.register('job-post',JobPostViewset,basename='job-post')
# router.register('interview',RecruiterProfileViewset,basename='recruiter-profile')

urlpatterns = [
    path('', include(router.urls)),
]