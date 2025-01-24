import requests
from logger_config import logger  # Логер тепер ізольований і не створює циклічного імпорту

class SWAPIClient:
    """Клас для отримання даних із SWAPI API."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_json(self, endpoint: str) -> list:
        """
        Отримує всі сторінки JSON-даних із вказаного endpoint.

        Args:
            endpoint (str): Кінцева точка API (наприклад, 'people' або 'planets').

        Returns:
            list: Список JSON-об'єктів із даними.
        """
        all_data = []
        url = f"{self.base_url}{endpoint}/"
        while url:
            try:
                logger.info(f"Отримання даних з: {url}")
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                all_data.extend(data.get("results", []))
                url = data.get("next")
            except requests.exceptions.RequestException as e:
                logger.error(f"Помилка при отриманні даних з {url}: {e}")
                break
        return all_data
