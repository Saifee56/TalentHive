import pytest
from rest_framework.test import APIClient
from authentication.models import CustomUserModel
from recruiter.models import RecruiterProfile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def recruiter_user(db):
    user=CustomUserModel.objects.create_user(
        username='recruiter_test',
        password='recruiter_test123',
        email='recruiter_test@gmail.com',
        role='recruiter',
        professional_bio='I am a pro'

    )
    return user

@pytest.fixture
def authenticated_client(api_client,recruiter_user):
    api_client.force_authenticate(user=recruiter_user)
    return api_client

@pytest.fixture
def recruiter_profile(recruiter_user):
    profile=RecruiterProfile.objects.create(
        user=recruiter_user,
        company_name="Test Company",
        company_website='https://testcompany.com',
        position='Hr manager',
        about_company='A test company description',
        company_size='50-100',
        industry='Technology',
        location='New York, USA'

    )
    return profile