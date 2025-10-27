
import pytest
from rest_framework.test import APIClient
from authentication.models import CustomUserModel

@pytest.fixture
def create_test_user():
    user=CustomUserModel.objects.create_user(
        username="saifee",
        password="saifee123",
        email="safuan@gmail.com",
        role="user"
    )
    return user

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
    
    def test_login_success(self,create_test_user):
        data={
            "email":create_test_user.email,
            "password":"saifee123"
        }

        response=self.client.post(self.login_url,data,format="json")
        assert response.status_code == 200
        assert response.data["success"]==True
        assert "access" in response.data["data"]
    
    def test_login_invalid_credentials(self,create_test_user):

        data1={
            "email":create_test_user.email,
            "password":"saifee12"
        }
        data2={
            "email":"safuan12345@gmail.com",
            "password":"saifee123"
        }

    @pytest.mark.parametrize("email,password,expected_status",[
        ("safuan@gmail.com","saifee12",401),
        ("safuan12345@gmail.com","saifee123",401),
    ])
    def test_login_invalid_credentials(self,create_test_user,email,password,expected_status):
        data={
            "email":email,
            "password":password
        }

        response=self.client.post(self.login_url,data,format="json")
        assert response.status_code==expected_status
        assert response.data["success"] is False