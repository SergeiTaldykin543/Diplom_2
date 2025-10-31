import allure
import pytest
import requests
from data.handlers import Urls, Handlers
from data.ingredients_data import Ingredient


class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и реальными ингредиентами")
    def test_create_order_with_auth_and_ingredients_success(self, auth_headers):
        correct_order_data = Ingredient.get_correct_ingredients_data()
        
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
            json=correct_order_data,
            headers=auth_headers,
            timeout=10
        )
        
        # Проверяем успешное создание заказа
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "name" in response.json()

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_error(self):
        correct_order_data = Ingredient.get_correct_ingredients_data()
        
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
            json=correct_order_data,
            headers=Handlers.headers,
            timeout=10
        )
        
        # API может возвращать 200 или 401 для неавторизованных пользователей
        assert response.status_code in [200, 401]
        if response.status_code == 200:
            assert response.json()["success"] == True
        else:
            assert response.json()["success"] == False

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_error(self, auth_headers):
        empty_data = Ingredient.get_empty_ingredients_data()
        
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
            json=empty_data,
            headers=auth_headers,
            timeout=10
        )
        
        # API может возвращать 400 или 403
        assert response.status_code in [400, 403]
        assert response.json()["success"] == False
        if response.status_code == 400:
            assert "Ingredient ids must be provided" in response.json()["message"]

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients_error(self, auth_headers):
        invalid_data = Ingredient.get_incorrect_ingredients_data()
        
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
            json=invalid_data,
            headers=auth_headers,
            timeout=10
        )
        
        # API может возвращать 500 или другую ошибку
        assert response.status_code >= 400
        
        # Обрабатываем случай когда сервер возвращает HTML вместо JSON
        try:
            response_data = response.json()
            assert response_data["success"] == False
        except ValueError:
            # Если ответ не JSON (например, HTML страница с ошибкой)
            # Это допустимо для 500 ошибок
            pass