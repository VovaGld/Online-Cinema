# Online-Cinema

## Як запустити проект

1. **Створи `.env` файл**:
   - Скопіюй вміст з `.env.sample` у новий `.env` файл.

2. **Налаштуй конфігурацію в IDE**:
   - Відкрий `Edit Configurations` у PyCharm.
   - вибери фаст апі
   - Додай змінні середовища з `.env` файлу до конфігурації запуску. не забуть зімнити хост на локал хост

3. **Запусти проект**:
   - Виконай команду `docker compose -f docker-compose-local.yml up --build` для запуску всіх сервісів.
   - Переконайся, що всі сервіси запущені та працюють коректно.
   - після чого запустити конфігурацію пайчарма з встановленими змінними енв

## Приклад `.env` файлу

```dotenv
#PostgreSQL
POSTGRES_DB=movies_db
POSTGRES_DB_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=some_password
POSTGRES_HOST=localhost
