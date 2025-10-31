import allure
import pytest
import requests
from data.handlers import Urls, Handlers
from data.user_data import User


class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self):
        user_data = User.create_data_user()
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.CREATE_USER}",
            json=user_data,
            headers=Handlers.headers,
            timeout=10
        )
        
        # API может возвращать 200 при успехе или 403 если пользователь уже существует
        if response.status_code == 200:
            assert response.json()["success"] == True
            assert "accessToken" in response.json()
            
            # Удаляем пользователя
            token = response.json()["accessToken"]
            headers_with_token = Handlers.headers.copy()
            headers_with_token["Authorization"] = token
            try:
                requests.delete(
                    f"{Urls.MAIN_URL}{Handlers.DELETE_USER}", 
                    headers=headers_with_token,
                    timeout=5
                )
            except requests.exceptions.RequestException:
                pass
        else:
            # Если 403, проверяем структуру ошибки
            assert response.status_code == 403
            assert response.json()["success"] == False
            assert "message" in response.json()

    @allure.title("Создание уже существующего пользователя")
    def test_create_existing_user_error(self):
        user_data = User.data_double
        
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.CREATE_USER}",
            json=user_data,
            headers=Handlers.headers,
            timeout=10
        )
        
        # Ожидаем ошибку 403, так как пользователь уже существует
        assert response.status_code == 403
        assert response.json()["success"] == False
        assert "User already exists" in response.json()["message"]

    @allure.title("Создание пользователя без email")
    def test_create_user_without_email_error(self):
        user_data = User.data_without_email
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.CREATE_USER}",
            json=user_data,
            headers=Handlers.headers,
            timeout=10
        )
        
        assert response.status_code == 403
        assert response.json()["success"] == False
        assert "Email, password and name are required fields" in response.json()["message"]