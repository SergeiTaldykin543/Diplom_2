import pytest
import allure
from data.handlers import ApiHandlers
from data.user_data import UserData
from data.expected_responses import ExpectedResponses


class TestLoginUser:
    
    @allure.title("Успешный логин пользователя с валидными данными")
    def test_login_user_success(self, authenticated_user):
        """Тест успешного входа в систему с валидными данными"""
        assert authenticated_user is not None, "Пользователь не был создан"
        
        # Сбрасываем токен и логинимся заново
        authenticated_user['client'].token = None
        response = authenticated_user['client'].login_user(
            authenticated_user['email'], 
            authenticated_user['password']
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] == True
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        assert response_data['user']['email'] == authenticated_user['email']
        assert response_data['user']['name'] == authenticated_user['name']
    
    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password(self, authenticated_user):
        """Тест входа с неверным паролем"""
        assert authenticated_user is not None, "Пользователь не был создан"
        
        # Пытаемся залогиниться с неверным паролем
        authenticated_user['client'].token = None
        response = authenticated_user['client'].login_user(
            authenticated_user['email'], 
            UserData.WRONG_PASSWORD
        )
        
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.INCORRECT_CREDENTIALS
    
    @allure.title("Логин с неверным email")
    def test_login_wrong_email(self, authenticated_user):
        """Тест входа с неверным email"""
        assert authenticated_user is not None, "Пользователь не был создан"
        
        # Пытаемся залогиниться с неверным email
        authenticated_user['client'].token = None
        response = authenticated_user['client'].login_user(
            UserData.WRONG_EMAIL, 
            authenticated_user['password']
        )
        
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.INCORRECT_CREDENTIALS
    
    @allure.title("Логин без пароля")
    def test_login_without_password(self, authenticated_user):
        """Тест входа без пароля"""
        assert authenticated_user is not None, "Пользователь не был создан"
        
        # Пытаемся залогиниться без пароля
        authenticated_user['client'].token = None
        response = authenticated_user['client'].login_user(
            authenticated_user['email'], 
            ""
        )
        
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.INCORRECT_CREDENTIALS