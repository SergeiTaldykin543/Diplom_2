import pytest
import allure
from data.handlers import ApiHandlers


class TestGetIngredients:
    
    @allure.title("Успешное получение списка ингредиентов")
    def test_get_ingredients_success(self):
        api = ApiHandlers()
        
        response = api.get_ingredients()
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] == True
        assert 'data' in response_data
        assert len(response_data['data']) > 0
        
        ingredient = response_data['data'][0]
        required_fields = ['_id', 'name', 'type', 'proteins', 'fat', 
                          'carbohydrates', 'calories', 'price', 'image', 
                          'image_mobile', 'image_large', '__v']
        
        for field in required_fields:
            assert field in ingredient, f"Отсутствует поле {field}"