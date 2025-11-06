import pytest
import allure
from data.handlers import ApiHandlers
from data.user_data import UserData
from data.expected_responses import ExpectedResponses


class TestCreateUser:
    
    @allure.title("Успешное создание пользователя с валидными данными")
    def test_create_user_success(self, unique_user_data):
        api = ApiHandlers()
        
        response = api.register_user(
            unique_user_data['email'],
            unique_user_data['password'],
            unique_user_data['name']
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] == True
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        assert response_data['user']['email'] == unique_user_data['email']
        assert response_data['user']['name'] == unique_user_data['name']
        
        api.login_user(unique_user_data['email'], unique_user_data['password'])
        api.delete_user()
    
    @allure.title("Создание пользователя с уже существующим email")
    def test_create_duplicate_user(self, authenticated_user):
        api = ApiHandlers()
        
        response = api.register_user(
            authenticated_user['email'],
            authenticated_user['password'],
            authenticated_user['name']
        )
        
        assert response.status_code == 403
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.USER_ALREADY_EXISTS
    
    @allure.title("Создание пользователя без email")
    def test_create_user_without_email(self):
        api = ApiHandlers()
        
        response = api.register_user("", UserData.PASSWORD, UserData.NAME)
        
        assert response.status_code == 403
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.REQUIRED_FIELDS
    
    @allure.title("Создание пользователя без пароля")
    def test_create_user_without_password(self):
        api = ApiHandlers()
        
        response = api.register_user(UserData.EMAIL, "", UserData.NAME)
        
        assert response.status_code == 403
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.REQUIRED_FIELDS
    
    @allure.title("Создание пользователя без имени")
    def test_create_user_without_name(self):
        api = ApiHandlers()
        
        response = api.register_user(UserData.EMAIL, UserData.PASSWORD, "")
        
        assert response.status_code == 403
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.REQUIRED_FIELDS