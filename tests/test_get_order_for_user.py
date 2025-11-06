import pytest
import allure
from data.ingredients_data import IngredientsData


class TestGetOrderForUser:
    
    @allure.title("Получение заказов пользователя с авторизацией")
    def test_get_user_orders_with_auth(self, user_with_order):
        client = user_with_order['client']
        
        assert client.token is not None, "Token should be set for authenticated user"
        print(f"Token in get orders test: {client.token}")
        
        response = client.get_user_orders()
        
        assert response is not None, "Response should not be None with valid token"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        
        response_data = response.json()
        assert response_data['success'] == True
        assert 'orders' in response_data
        assert 'total' in response_data
        assert 'totalToday' in response_data
        
        if len(response_data['orders']) > 0:
            order = response_data['orders'][0]
            required_order_fields = ['ingredients', '_id', 'status', 'number', 'createdAt', 'updatedAt']
            for field in required_order_fields:
                assert field in order, f"Отсутствует поле {field} в заказе"
    
    @allure.title("Получение заказов пользователя без авторизации")
    def test_get_user_orders_without_auth(self, fresh_api_client):
        client = fresh_api_client
        response = client.get_user_orders()
        assert response is None
    
    @allure.title("Получение всех заказов")
    def test_get_all_orders(self, fresh_api_client):
        client = fresh_api_client
        response = client.get_all_orders()
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        response_data = response.json()
        assert response_data['success'] == True
        assert 'orders' in response_data
        assert 'total' in response_data
        assert 'totalToday' in response_data