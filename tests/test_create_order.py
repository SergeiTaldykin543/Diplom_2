import pytest
import allure
from data.ingredients_data import IngredientsData
from data.expected_responses import ExpectedResponses


class TestCreateOrder:
    
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, user_with_order):
        """Тест создания заказа авторизованным пользователем"""
        # Убедимся что у нас есть ингредиенты
        assert len(IngredientsData.VALID_INGREDIENTS) > 0, "Нет доступных ингредиентов"
        
        response = user_with_order['client'].create_order(IngredientsData.VALID_INGREDIENTS)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        response_data = response.json()
        assert response_data['success'] == True
        assert 'name' in response_data
        assert 'order' in response_data
        assert 'number' in response_data['order']
    
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, api_client):
        """Тест создания заказа без авторизации"""
        # Сначала получаем ингредиенты
        ingredients_response = api_client.get_ingredients()
        assert ingredients_response.status_code == 200
        assert len(IngredientsData.VALID_INGREDIENTS) > 0
        
        response = api_client.create_order(IngredientsData.VALID_INGREDIENTS)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        response_data = response.json()
        assert response_data['success'] == True
    
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, authenticated_user):
        """Тест создания заказа без ингредиентов"""
        response = authenticated_user['client'].create_order(IngredientsData.EMPTY_INGREDIENTS)
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
        response_data = response.json()
        assert response_data['success'] == False
        assert response_data['message'] == ExpectedResponses.INGREDIENTS_REQUIRED
    
    @allure.title("Создание заказа с невалидными ингредиентами")
    def test_create_order_invalid_ingredients(self, authenticated_user):
        """Тест создания заказа с невалидными ингредиентами"""
        response = authenticated_user['client'].create_order(IngredientsData.INVALID_INGREDIENTS)
        
        # API может возвращать 500 для невалидных ингредиентов
        assert response.status_code in [400, 500], f"Expected 400 or 500, got {response.status_code}. Response: {response.text}"