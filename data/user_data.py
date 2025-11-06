class UserData:
    BASE_URL = "https://stellarburgers.education-services.ru"
    
    # Основные тестовые данные
    EMAIL = "sergey_31@test.ru"
    PASSWORD = "1234567S"
    NAME = "Taldykin_31"
    
    # Данные для обновления
    NEW_EMAIL = "new_sergey_31@test.ru"
    NEW_PASSWORD = "new1234567S"
    NEW_NAME = "New_Taldykin_31"
    
    # Невалидные данные для тестов
    INVALID_EMAIL = "invalid_email"
    INVALID_PASSWORD = "123"
    EMPTY_FIELD = ""
    WRONG_EMAIL = "wrong@email.com"
    WRONG_PASSWORD = "wrong_password"
    
    # API endpoints
    CREATE_USER_URL = "/api/auth/register"
    LOGIN_URL = "/api/auth/login"
    USER_URL = "/api/auth/user"
    LOGOUT_URL = "/api/auth/logout"
    TOKEN_URL = "/api/auth/token"
    ORDERS_URL = "/api/orders"
    ORDERS_ALL_URL = "/api/orders/all"
    INGREDIENTS_URL = "/api/ingredients"
    PASSWORD_RESET_URL = "/api/password-reset"