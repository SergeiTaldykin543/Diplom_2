class IngredientsData:
    VALID_INGREDIENTS = []
    
    INVALID_INGREDIENTS = ["invalid_hash_1", "invalid_hash_2"]
    EMPTY_INGREDIENTS = []
    
    @classmethod
    def set_valid_ingredients(cls, ingredients_list):
        cls.VALID_INGREDIENTS = ingredients_list