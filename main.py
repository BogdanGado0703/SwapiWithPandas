import argparse
import json
from Swapi_client import SWAPIClient
from Swapi_Data_Manager import SWAPIDataManager
from logger_config import logger  # Імпортуємо логер

def main():
    parser = argparse.ArgumentParser(description="Завантаження даних із SWAPI API та збереження в Excel.")
    parser.add_argument("--endpoint", type=str, required=False, default="people,planets",
                        help="Список сутностей через кому (наприклад, people,planets)")
    parser.add_argument("--output", type=str, required=False, default="swapi_data.xlsx",
                        help="Ім'я вихідного Excel-файлу")
    parser.add_argument("--filters", type=str,
                        default='{"people": ["films", "species"], "planets": ["films", "residents"]}',
                        help="JSON-рядок із фільтрами для кожної сутності")
    args = parser.parse_args()
    endpoints = args.endpoint.split(",")
    output_file = args.output
    filters = json.loads(args.filters)

    client = SWAPIClient(base_url="https://swapi.dev/api/")
    manager = SWAPIDataManager(client)

    for endpoint in endpoints:
        logger.info(f"Обробка сутності: {endpoint}")
        manager.fetch_entity(endpoint)
        if endpoint in filters:
            manager.apply_filter(endpoint, filters[endpoint])

    manager.save_to_excel("C:/Users/User/OneDrive/Робочий стіл/SWAPIClient.xlsx")


if __name__ == "__main__":
    main()
