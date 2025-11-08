import pytest
import allure
from data.ingredients_data import IngredientsData


class TestGetOrderForUser:
    
    @allure.title("Получение заказов пользователя с заказом")
    def test_get_user_orders_with_order(self, user_with_order):
        client = user_with_order['client']
        
        response = client.get_user_orders()
        
        assert response is not None
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data['success'] == True
        assert 'orders' in response_data
        assert 'total' in response_data
        assert 'totalToday' in response_data
        assert len(response_data['orders']) > 0
        
        order = response_data['orders'][0]
        required_order_fields = ['ingredients', '_id', 'status', 'number', 'createdAt', 'updatedAt']
        for field in required_order_fields:
            assert field in order
    
    @allure.title("Получение заказов пользователя без заказов")
    def test_get_user_orders_without_orders(self, authenticated_user):
        client = authenticated_user['client']
        
        response = client.get_user_orders()
        
        assert response is not None
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data['success'] == True
        assert 'orders' in response_data
        assert len(response_data['orders']) == 0
    
    @allure.title("Получение заказов пользователя без авторизации")
    def test_get_user_orders_without_auth(self, api_client):
        client = api_client
        response = client.get_user_orders()
        assert response is None
    
    @allure.title("Получение всех заказов")
    def test_get_all_orders(self, api_client):
        client = api_client
        response = client.get_all_orders()
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] == True
        assert 'orders' in response_data
        assert 'total' in response_data
        assert 'totalToday' in response_data