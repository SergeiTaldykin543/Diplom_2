import allure
import pytest
import requests
from data.handlers import Urls, Handlers
from data.user_data import User


class TestLoginUser:
    @allure.title("Успешный логин под существующим пользователем")
    def test_login_existing_user_success(self, create_and_delete_user):
        user_data, _ = create_and_delete_user
        
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        try:
            response = requests.post(
                f"{Urls.MAIN_URL}{Handlers.LOGIN}",
                json=login_data,
                headers=Handlers.headers,
                timeout=10
            )
        except requests.exceptions.RequestException:
            pytest.fail("Не удалось выполнить логин")
            return
        
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "accessToken" in response.json()

    @allure.title("Логин с неверным email")
    def test_login_with_wrong_email_error(self):
        login_data = User.data_negative
        
        try:
            response = requests.post(
                f"{Urls.MAIN_URL}{Handlers.LOGIN}",
                json=login_data,
                headers=Handlers.headers,
                timeout=10
            )
        except requests.exceptions.RequestException:
            pytest.fail("Не удалось выполнить логин")
            return
        
        assert response.status_code == 401
        assert response.json()["success"] == False

    @allure.title("Логин с неверным паролем")
    def test_login_with_wrong_password_error(self, create_and_delete_user):
        user_data, _ = create_and_delete_user
        
        login_data = {
            "email": user_data["email"],
            "password": "wrong_password"
        }
        
        try:
            response = requests.post(
                f"{Urls.MAIN_URL}{Handlers.LOGIN}",
                json=login_data,
                headers=Handlers.headers,
                timeout=10
            )
        except requests.exceptions.RequestException:
            pytest.fail("Не удалось выполнить логин")
            return
        
        assert response.status_code == 401
        assert response.json()["success"] == False

    @allure.title("Логин без email")
    def test_login_without_email_error(self):
        login_data = {"email": "", "password": "password"}
        
        try:
            response = requests.post(
                f"{Urls.MAIN_URL}{Handlers.LOGIN}",
                json=login_data,
                headers=Handlers.headers,
                timeout=10
            )
        except requests.exceptions.RequestException:
            pytest.fail("Не удалось выполнить логин")
            return
        
        assert response.status_code == 401
        assert response.json()["success"] == False

    @allure.title("Логин без пароля")
    def test_login_without_password_error(self):
        login_data = {"email": "test@yandex.ru", "password": ""}
        
        try:
            response = requests.post(
                f"{Urls.MAIN_URL}{Handlers.LOGIN}",
                json=login_data,
                headers=Handlers.headers,
                timeout=10
            )
        except requests.exceptions.RequestException:
            pytest.fail("Не удалось выполнить логин")
            return
        
        assert response.status_code == 401
        assert response.json()["success"] == False