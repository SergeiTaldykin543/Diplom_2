class Urls:
    MAIN_URL = 'https://stellarburgers.education-services.ru'  # Правильный хост из документации


class Handlers:
    CREATE_USER = '/api/auth/register'
    LOGIN = '/api/auth/login'
    CHANGE_USER_DATA = '/api/auth/user'
    DELETE_USER = '/api/auth/user'
    MAKE_ORDER = '/api/orders'
    GET_ORDERS = '/api/orders'
    GET_ALL_ORDERS = '/api/orders/all'
    INGREDIENTS = '/api/ingredients'
    
    headers = {"Content-Type": "application/json"}