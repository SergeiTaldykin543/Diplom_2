import pytest
import requests
from data.handlers import Urls, Handlers
from data.user_data import User


@pytest.fixture
def create_and_delete_user():
    """Фикстура для создания и последующего удаления пользователя"""
    user_data = User.create_data_user()
    create_response = requests.post(f"{Urls.MAIN_URL}{Handlers.CREATE_USER}", 
                                   json=user_data, 
                                   headers=Handlers.headers)
    
    token = None
    if create_response.status_code == 200:
        token = create_response.json()["accessToken"]
    
    yield user_data, token
    
    # Удаляем пользователя после теста
    if token:
        headers_with_token = Handlers.headers.copy()
        headers_with_token["Authorization"] = token
        requests.delete(f"{Urls.MAIN_URL}{Handlers.DELETE_USER}", 
                       headers=headers_with_token)


@pytest.fixture
def auth_headers(create_and_delete_user):
    """Фикстура для получения заголовков с авторизацией"""
    _, token = create_and_delete_user
    headers = Handlers.headers.copy()
    if token:
        headers["Authorization"] = token
    return headers


@pytest.fixture
def registered_user():
    """Фикстура для зарегистрированного пользователя с известными данными"""
    # Сначала пытаемся удалить пользователя если он существует
    login_data = {
        "email": User.data_correct["email"],
        "password": User.data_correct["password"]
    }
    
    # Пробуем залогиниться
    login_response = requests.post(f"{Urls.MAIN_URL}{Handlers.LOGIN}", 
                                  json=login_data, 
                                  headers=Handlers.headers)
    
    if login_response.status_code == 200:
        # Если пользователь существует, удаляем его
        token = login_response.json()["accessToken"]
        headers_with_token = Handlers.headers.copy()
        headers_with_token["Authorization"] = token
        requests.delete(f"{Urls.MAIN_URL}{Handlers.DELETE_USER}", 
                       headers=headers_with_token)
    
    # Регистрируем нового пользователя
    create_response = requests.post(f"{Urls.MAIN_URL}{Handlers.CREATE_USER}", 
                                   json=User.data_correct, 
                                   headers=Handlers.headers)
    
    token = None
    if create_response.status_code == 200:
        token = create_response.json()["accessToken"]
    
    yield User.data_correct, token
    
    # Удаляем пользователя после теста
    if token:
        headers_with_token = Handlers.headers.copy()
        headers_with_token["Authorization"] = token
        requests.delete(f"{Urls.MAIN_URL}{Handlers.DELETE_USER}", 
                       headers=headers_with_token)