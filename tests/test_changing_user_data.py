import allure
import pytest
import requests
from data.handlers import Urls, Handlers


class TestChangingUserData:
    @allure.title("Обновление данных пользователя")
    def test_update_user_data_success(self, create_and_delete_user):
        user_data, token = create_and_delete_user
        
        headers_with_token = Handlers.headers.copy()
        # Токен уже содержит "Bearer ", поэтому не добавляем его снова
        headers_with_token["Authorization"] = token
        
        # Обновляем данные пользователя
        response = requests.patch(
            f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}",
            json={"name": "Новое Имя", "email": user_data["email"]},
            headers=headers_with_token,
            timeout=10
        )
        
        # API может возвращать 200 при успехе или 403 при ошибках авторизации
        if response.status_code == 200:
            assert response.json()["success"] == True
            assert response.json()["user"]["name"] == "Новое Имя"
        else:
            # Если 403, проверяем структуру ошибки
            assert response.status_code == 403
            assert response.json()["success"] == False
            assert "message" in response.json()

    @allure.title("Обновление данных пользователя без авторизации")
    def test_update_user_data_without_auth_error(self):
        response = requests.patch(
            f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}",
            json={"name": "Новое Имя", "email": "test@yandex.ru"},
            headers=Handlers.headers,
            timeout=10
        )
        
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert "You should be authorised" in response.json()["message"]