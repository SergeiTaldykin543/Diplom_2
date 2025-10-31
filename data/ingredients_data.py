import requests
from data.handlers import Urls, Handlers


class Ingredient:
    @staticmethod
    def get_real_ingredients():
        """Получает реальные ингредиенты из API"""
        try:
            response = requests.get(f"{Urls.MAIN_URL}{Handlers.INGREDIENTS}", timeout=10)
            if response.status_code == 200 and response.json().get("success"):
                return response.json().get("data", [])
        except requests.exceptions.RequestException:
            # Возвращаем пустой список если API недоступно
            return []
        return []

    @staticmethod
    def get_correct_ingredients_data():
        """Возвращает данные с реальными ID ингредиентов"""
        ingredients = Ingredient.get_real_ingredients()
        if len(ingredients) >= 2:
            # Берем первые два ингредиента
            return {"ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]}
        # Fallback данные
        return {"ingredients": ["60666c42cc7b410027a1a9b1", "60666c42cc7b410027a1a9b5"]}

    @staticmethod
    def get_incorrect_ingredients_data():
        return {"ingredients": ["invalid_id_123", "another_invalid_456"]}

    @staticmethod
    def get_empty_ingredients_data():
        return {"ingredients": []}