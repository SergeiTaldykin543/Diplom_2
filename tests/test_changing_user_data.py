import pytest
import allure
from data.user_data import UserData
from data.handlers import ApiHandlers


class TestChangingUserData:
    
    @allure.title("Получение данных пользователя с авторизацией")
    def test_get_user_info_with_auth(self, authenticated_user):
        client = authenticated_user['client']
        
        response = client.get_user_info()
        
        assert response is not None
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data['success'] == True
        assert response_data['user']['email'] == authenticated_user['email']
        assert response_data['user']['name'] == authenticated_user['name']
    
    @allure.title("Обновление email пользователя")
    def test_update_user_email(self, authenticated_user):
        client = authenticated_user['client']
        new_email = client.generate_unique_email()
        
        response = client.update_user_email(new_email)
        
        assert response is not None
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data['success'] == True
        assert response_data['user']['email'] == new_email
        assert response_data['user']['name'] == authenticated_user['name']
    
    @allure.title("Обновление имени пользователя")
    def test_update_user_name(self, authenticated_user):
        client = authenticated_user['client']
        
        response = client.update_user_name(UserData.NEW_NAME)
        
        assert response is not None
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data['success'] == True
        assert response_data['user']['email'] == authenticated_user['email']
        assert response_data['user']['name'] == UserData.NEW_NAME
    
    @allure.title("Обновление пароля пользователя")
    def test_update_user_password(self, authenticated_user):
        client = authenticated_user['client']
        
        response = client.update_user_password(UserData.NEW_PASSWORD)
        
        assert response is not None
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data['success'] == True
    
    @allure.title("Обновление данных без авторизации")
    def test_update_user_info_without_auth(self, api_client, unique_user_data):
        client = api_client
        
        register_response = client.register_user(
            unique_user_data['email'],
            unique_user_data['password'],
            unique_user_data['name']
        )
        
        client.token = None
        
        response = client.update_user_info(email=UserData.NEW_EMAIL)
        
        assert response is None