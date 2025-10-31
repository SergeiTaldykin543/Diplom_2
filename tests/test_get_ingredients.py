import allure
import pytest
import requests
from data.handlers import Urls, Handlers
from data.ingredients_data import Ingredient


class TestGetIngredients:
    @allure.title("Получение данных об ингредиентах")
    def test_get_ingredients_success(self):
        # Получаем ингредиенты напрямую в тесте
        ingredients = Ingredient.get_real_ingredients()
        
        # Если API недоступно, тест будет пропущен
        assert len(ingredients) > 0, "Список ингредиентов пуст"
        
        # Проверяем структуру ингредиентов
        for ingredient in ingredients[:3]:
            assert "_id" in ingredient
            assert "name" in ingredient
            assert "type" in ingredient

    @allure.title("Получение ингредиентов проверяет структуру ответа")
    def test_get_ingredients_structure(self):
        try:
            response = requests.get(
                f"{Urls.MAIN_URL}{Handlers.INGREDIENTS}",
                timeout=10
            )
        except requests.exceptions.RequestException:
            pytest.fail("Не удалось получить ингредиенты")
            return
        
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "data" in response.json()