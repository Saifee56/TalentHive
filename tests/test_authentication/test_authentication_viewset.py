
import pytest
from rest_framework.test import APIClient
from authentication.models import CustomUserModel

@pytest.mark.django_db
class TestAuthenticationViewset:

    def setup_method(self):
        self.client=APIClient()
        self.signup_url="/api/authentication/auth/signup/"
        self.login_url="/api/authentication/auth/login/"
    
    def test_signup_success(self):
        data={
            "username":"test",
            "email":"test@gmail.com",
            "first_name":"test_data",
            "last_name":"sheet",
            "password":"strongpassword",
            "role":"job_seeker",
            "professional_bio":"I am test"
        }

        response=self.client.post(self.signup_url,data,format="json")

        assert response.status_code == 201
        assert response.data["success"] is True
        assert "access" in response.data["data"]
        assert CustomUserModel.objects.filter(email="test@gmail.com").exists()
    
    def test_signup_failure_missing_fileds(self):
        data={
            "username":"test",
            "role":"job_seeker"
        }

        response=self.client.post(self.signup_url,data,format="json")
        assert response.status_code == 400
        assert response.data["success"] is False
        assert response.data["message"]=="Signup failed"
        assert "errors" in response.data