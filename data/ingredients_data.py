class IngredientsData:
    # Примеры валидных ингредиентов (будут получены динамически)
    VALID_INGREDIENTS = []
    
    # Невалидные ингредиенты
    INVALID_INGREDIENTS = ["invalid_hash_1", "invalid_hash_2"]
    EMPTY_INGREDIENTS = []
    
    @classmethod
    def set_valid_ingredients(cls, ingredients_list):
        """Устанавливает валидные ингредиенты из API"""
        cls.VALID_INGREDIENTS = ingredients_list