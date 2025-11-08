import pytest
import random
import string
from data.handlers import ApiHandlers
from data.user_data import UserData
from data.ingredients_data import IngredientsData


def generate_unique_email():
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{random_suffix}@test.ru"


@pytest.fixture
def api_client():
    return ApiHandlers()


@pytest.fixture
def unique_user_data():
    return {
        'email': generate_unique_email(),
        'password': UserData.PASSWORD,
        'name': UserData.NAME
    }


@pytest.fixture
def registered_user(api_client, unique_user_data):
    client = api_client
    
    register_response = client.register_user(
        unique_user_data['email'],
        unique_user_data['password'],
        unique_user_data['name']
    )
    
    return {
        'client': client,
        'email': unique_user_data['email'],
        'password': unique_user_data['password'],
        'name': unique_user_data['name']
    }


@pytest.fixture
def authenticated_user(registered_user):
    client = registered_user['client']
    
    login_response = client.login_user(
        registered_user['email'],
        registered_user['password']
    )
    
    yield registered_user
    
    if client.token:
        client.delete_user()


@pytest.fixture
def user_with_order(authenticated_user):
    client = authenticated_user['client']
    
    ingredients_response = client.get_ingredients()
    
    order_response = client.create_order(IngredientsData.VALID_INGREDIENTS)
    
    yield authenticated_user