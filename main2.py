import pandas as pd
import requests
import logging
import argparse
import os

# Налаштування логера
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SWAPIClient:
    def __init__(self, path: str):
        self.base_url = path

    def fetch_json(self, endpoint: str) -> list:
        all_data = []
        url = f"{self.base_url}/{endpoint}/"  # Оновлене формування URL

        while url:
            logger.info(f"Отримання даних з: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_data.extend(data['results'])
            url = data.get('next')

        return all_data


class ExcelSWAPIClient(SWAPIClient):
    def __init__(self, path: str):
        super().__init__(path)
        self.file_path = path

    def fetch_json(self, endpoint: str) -> list:
        logger.info(f"Читання даних із файлу: {self.file_path}, лист: {endpoint}")
        try:
            df = pd.read_excel(self.file_path, sheet_name=endpoint.capitalize())
            return df.to_dict(orient='records')
        except ValueError:
            logger.warning(f"Endpoint {endpoint} not found in {self.file_path}")
            return []



class SWAPIDataManager:
    def __init__(self, client: SWAPIClient):
        self.client = client
        self.data = {}

    def fetch_entity(self, endpoint: str):
        self.data[endpoint] = pd.DataFrame(self.client.fetch_json(endpoint))

    def save_to_excel(self, filename: str):
        with pd.ExcelWriter(filename) as writer:
            for endpoint, df in self.data.items():
                df.to_excel(writer, sheet_name=endpoint.capitalize(), index=False)
        logger.info(f"Дані збережено у файл: {filename}")

        def get_client(input_source: str):
            if input_source.startswith("http"):
                return SWAPIClient(input_source)
            elif input_source.endswith(".xlsx"):
                return ExcelSWAPIClient(input_source)
            else:
                raise ValueError("Невідомий формат джерела даних")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="URL API або шлях до Excel-файлу")
    parser.add_argument("--endpoint", required=True, help="Список сутностей через кому (people,planets,films)")
    parser.add_argument("--output", required=True, help="Ім'я вихідного Excel-файлу")
    args = parser.parse_args()

    if args.input.startswith("http"):
        client = SWAPIClient(args.input)
    else:
        client = ExcelSWAPIClient(args.input)

    manager = SWAPIDataManager(client)
    for endpoint in args.endpoint.split(","):
        manager.fetch_entity(endpoint)

    manager.save_to_excel(args.output)
