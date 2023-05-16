Создание docker-image и docker-compose для [предыдущего примера](https://gitlab.com/golodnyuk.iv/db_2022/-/tree/main/%D0%9C%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%20%D0%BF%D0%BE%20%D0%BA%D1%83%D1%80%D1%81%D1%83/%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80%20CRUD%20%D1%81%20%D0%BA%D1%8D%D1%88%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%D0%BC%20%D0%B2%20Redis):

1. Создать `.env` файл, пример заполнения:
```dotenv
APP_NAME=lab-app-yourname
APP_PORT=12862

POSTGRES_PORT=34351
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=WrN7VXMcNnkqHSyQ

REDIS_PORT=40379
REDIS_PASSWORD=nTJpmYU4WSfFsFw2
```

2. Если сделана десериализация, то [изменить Dockerfile](https://gitlab.com/golodnyuk.iv/db_2022/-/blob/main/%D0%9C%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%20%D0%BF%D0%BE%20%D0%BA%D1%83%D1%80%D1%81%D1%83/Containerized%20Flask/Dockerfile#L10)

3. Убедиться в [requirements.txt](https://gitlab.com/golodnyuk.iv/db_2022/-/blob/main/%D0%9C%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%20%D0%BF%D0%BE%20%D0%BA%D1%83%D1%80%D1%81%D1%83/Containerized%20Flask/requirements.txt) прописаны нужные пакеты

4. Изменить [строки подключения](https://gitlab.com/golodnyuk.iv/db_2022/-/blob/main/%D0%9C%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%20%D0%BF%D0%BE%20%D0%BA%D1%83%D1%80%D1%81%D1%83/Containerized%20Flask/main.py#L13)
