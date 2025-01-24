import pandas as pd
from logger_config import logger


class SWAPIDataManager:
    """Клас для обробки даних і збереження в Excel."""

    def __init__(self, client):
        self.client = client
        self.data = {}

    def fetch_entity(self, endpoint: str):
        """
        Завантажує дані із вказаного endpoint та перетворює їх у DataFrame.
        """
        json_data = self.client.fetch_json(endpoint)
        if json_data:
            self.data[endpoint] = pd.DataFrame(json_data)
        else:
            logger.warning(f"Не вдалося отримати дані для {endpoint}")

    def apply_filter(self, endpoint: str, columns_to_drop: list):
        """
        Видаляє вказані стовпці з DataFrame.
        """
        if endpoint in self.data:
            logger.info(f"Застосування фільтрів для '{endpoint}': видалення {columns_to_drop}")
            self.data[endpoint].drop(columns=columns_to_drop, inplace=True, errors="ignore")

    def save_to_excel(self, filename: str):
        """
        Зберігає всі зібрані дані в Excel файл.
        """
        logger.info(f"Запис даних у файл Excel: {filename}")

        # Перевіримо, чи є дані для кожного ендпоінта
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for endpoint, df in self.data.items():
                if not df.empty:
                    sheet_name = endpoint.capitalize()
                    logger.info(f"Записуємо {len(df)} записів для {endpoint} в лист {sheet_name}")
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    logger.warning(f"Для {endpoint} немає даних для запису.")
        logger.info("Дані успішно записано у Excel.")
