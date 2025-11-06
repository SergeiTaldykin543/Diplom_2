import requests
import allure
import random
import string
from data.user_data import UserData
from data.ingredients_data import IngredientsData


class ApiHandlers:
    def __init__(self):
        self.base_url = UserData.BASE_URL
        self.token = None
    
    def _generate_unique_email(self):
        """Генерирует уникальный email для тестов"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"test_{random_suffix}@test.ru"
    
    def _get_headers(self):
        """Возвращает заголовки с токеном если он есть"""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'{self.token}'
        return headers
    
    @allure.step("Регистрация пользователя")
    def register_user(self, email, password, name):
        url = f"{self.base_url}{UserData.CREATE_USER_URL}"
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            # Сохраняем токен как есть (API возвращает его с 'Bearer ')
            self.token = data.get('accessToken')
            print(f"Token after registration: {self.token}")
        
        return response
    
    @allure.step("Логин пользователя")
    def login_user(self, email, password):
        url = f"{self.base_url}{UserData.LOGIN_URL}"
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            # Сохраняем токен как есть
            self.token = data.get('accessToken')
            print(f"Token after login: {self.token}")
        
        return response
    
    @allure.step("Удаление пользователя")
    def delete_user(self):
        if not self.token:
            print("No token available for deletion")
            return None
            
        url = f"{self.base_url}{UserData.USER_URL}"
        headers = self._get_headers()
        response = requests.delete(url, headers=headers)
        print(f"Delete user response: {response.status_code}")
        return response
    
    @allure.step("Получение информации о пользователе")
    def get_user_info(self):
        if not self.token:
            print("No token available for get_user_info")
            return None
            
        url = f"{self.base_url}{UserData.USER_URL}"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        print(f"Get user info response: {response.status_code}, token: {self.token}")
        return response
    
    @allure.step("Обновление информации о пользователе")
    def update_user_info(self, email=None, name=None, password=None):
        if not self.token:
            print("No token available for update_user_info")
            return None
            
        url = f"{self.base_url}{UserData.USER_URL}"
        headers = self._get_headers()
        
        payload = {}
        if email is not None:
            payload['email'] = email
        if name is not None:
            payload['name'] = name
        if password is not None:
            payload['password'] = password
            
        response = requests.patch(url, headers=headers, json=payload)
        print(f"Update user info response: {response.status_code}")
        return response
    
    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        url = f"{self.base_url}{UserData.INGREDIENTS_URL}"
        response = requests.get(url)
        
        # Сохраняем ингредиенты для использования в тестах
        if response.status_code == 200:
            ingredients_list = [ingredient['_id'] for ingredient in response.json()['data'][:2]]
            IngredientsData.set_valid_ingredients(ingredients_list)
        
        return response
    
    @allure.step("Создание заказа")
    def create_order(self, ingredients):
        url = f"{self.base_url}{UserData.ORDERS_URL}"
        headers = self._get_headers()
            
        payload = {"ingredients": ingredients}
        response = requests.post(url, headers=headers, json=payload)
        print(f"Create order response: {response.status_code}")
        return response
    
    @allure.step("Получение заказов пользователя")
    def get_user_orders(self):
        if not self.token:
            print("No token available for get_user_orders")
            return None
            
        url = f"{self.base_url}{UserData.ORDERS_URL}"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        print(f"Get user orders response: {response.status_code}")
        return response
    
    @allure.step("Получение всех заказов")
    def get_all_orders(self):
        url = f"{self.base_url}{UserData.ORDERS_ALL_URL}"
        response = requests.get(url)
        return response