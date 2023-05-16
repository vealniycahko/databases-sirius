# создание и запуск контейнера с postgresql
docker run --name postgres_db2022 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 38746:5432 -d postgres

docker ps # список запущенных контейнеров
docker ps -a # список всех контейнеров

docker stop postgres_db2022 # остановка контейнера
docker start postgres_db2022 # запуск остановленного контейнера
docker rm postgres_db2022 # удаление контейнера


# создание и запуск контейнера с redis
docker run --name redis_db2022 -p 26596:6379 -d redis --requirepass redis

#подключение к redis-cli
docker exec -it redis_db2022 redis-cli -a 'redis' # здесь -a 'redis' означает использования пароля redis


# создание и запуск контейнера с mongodb
docker run --name mongo_db2022 -e MONGO_INITDB_ROOT_USERNAME=mongo -e MONGO_INITDB_ROOT_PASSWORD=mongo -p 37112:27017 -d mongo
