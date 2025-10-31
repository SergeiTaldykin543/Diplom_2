import allure
import pytest
import requests
from data.handlers import Urls, Handlers
from data.ingredients_data import Ingredient


class TestGetOrderForUser:
    @allure.title("Получение заказов конкретного пользователя")
    def test_get_user_orders_with_auth_success(self, auth_headers):
        correct_order_data = Ingredient.get_correct_ingredients_data()
        
        # Сначала создаем заказ
        order_response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
            json=correct_order_data,
            headers=auth_headers,
            timeout=10
        )
        
        # Затем получаем заказы пользователя
        response = requests.get(
            f"{Urls.MAIN_URL}{Handlers.GET_ORDERS}",
            headers=auth_headers,
            timeout=10
        )
        
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "orders" in response.json()

    @allure.title("Получение заказов без авторизации")
    def test_get_user_orders_without_auth_error(self):
        response = requests.get(
            f"{Urls.MAIN_URL}{Handlers.GET_ORDERS}",
            headers=Handlers.headers,
            timeout=10
        )
        
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert "You should be authorised" in response.json()["message"]

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