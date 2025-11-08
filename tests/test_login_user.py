import pytest
import allure
from data.handlers import ApiHandlers
from data.user_data import UserData
from data.expected_responses import ExpectedResponses


class TestLoginUser:
    
    @allure.title("Успешный логин пользователя с валидными данными")
    def test_login_user_success(self, registered_user):
        registered_user['client'].token = None
        response = registered_user['client'].login_user(
            registered_user['email'], 
            registered_user['password']
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] == True
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        assert response_data['user']['email'] == registered_user['email']
        assert response_data['user']['name'] == registered_user['name']
    
    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password(self, registered_user):
        registered_user['client'].token = None
        response = registered_user['client'].login_user(
            registered_user['email'], 
            UserData.WRONG_PASSWORD
        )
        
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.INCORRECT_CREDENTIALS
    
    @allure.title("Логин с неверным email")
    def test_login_wrong_email(self, registered_user):
        registered_user['client'].token = None
        response = registered_user['client'].login_user(
            UserData.WRONG_EMAIL, 
            registered_user['password']
        )
        
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.INCORRECT_CREDENTIALS
    
    @allure.title("Логин без пароля")
    def test_login_without_password(self, registered_user):
        registered_user['client'].token = None
        response = registered_user['client'].login_user(
            registered_user['email'], 
            ""
        )
        
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.INCORRECT_CREDENTIALS