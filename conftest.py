import pytest
import random
import string
from data.handlers import ApiHandlers


def _generate_unique_email():
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{random_suffix}@test.ru"


@pytest.fixture
def api_client():
    return ApiHandlers()


@pytest.fixture
def unique_user_data():
    from data.user_data import UserData
    return {
        'email': _generate_unique_email(),
        'password': UserData.PASSWORD,
        'name': UserData.NAME
    }


@pytest.fixture
def fresh_api_client():
    return ApiHandlers()


@pytest.fixture
def registered_user(fresh_api_client, unique_user_data):
    client = fresh_api_client
    
    register_response = client.register_user(
        unique_user_data['email'],
        unique_user_data['password'],
        unique_user_data['name']
    )
    
    assert register_response.status_code == 200, f"Registration failed: {register_response.text}"
    
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
    
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    assert client.token is not None, "Token should be set after login"
    
    yield registered_user
    
    if client.token:
        delete_response = client.delete_user()
        if delete_response and delete_response.status_code not in [200, 202]:
            print(f"Warning: Failed to delete user: {delete_response.status_code}")


@pytest.fixture
def user_with_order(authenticated_user):
    client = authenticated_user['client']
    
    ingredients_response = client.get_ingredients()
    assert ingredients_response.status_code == 200, "Failed to get ingredients"
    
    from data.ingredients_data import IngredientsData
    assert len(IngredientsData.VALID_INGREDIENTS) > 0, "No valid ingredients available"
    
    order_response = client.create_order(IngredientsData.VALID_INGREDIENTS)
    assert order_response.status_code == 200, f"Failed to create order: {order_response.text}"
    
    return authenticated_user


def pytest_configure(config):
    config.option.allure_report_dir = "allure-results"


def pytest_unconfigure(config):
    pass