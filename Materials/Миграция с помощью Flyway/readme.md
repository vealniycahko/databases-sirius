Создаем папку migrations и добавляем туда sql файлы миграций, как сделано в данном примере. Про naming conventions можно почитать [тут](https://flywaydb.org/documentation/concepts/migrations#naming)

Устанавливаем Flyway ([source](https://flywaydb.org/documentation/usage/commandline/#download-and-installation)):
```shell
sudo wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/9.4.0/flyway-commandline-9.4.0-linux-x64.tar.gz | tar xvz && sudo ln -s `pwd`/flyway-9.4.0/flyway /usr/local/bin 
```

Добавляем .env файл в котором заданы `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, например:

```env
POSTGRES_PORT=38746
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

Запускаем миграции командой:
```shell
export $(grep -v '^#' .env | xargs) && flyway migrate -url=jdbc:postgresql://127.0.0.1:${POSTGRES_PORT}/${POSTGRES_DB} -user=${POSTGRES_USER} -password=${POSTGRES_PASSWORD} -locations="filesystem:./migrations" 
```

По-умолчанию Flyway откажется проводить миграции, если уже есть какие-либо другие таблицы в базе. Для того, чтобы
отключить эту проверку, нужно добавить флаг `baselineOnMigrate` со значением `true`:
```shell
export $(grep -v '^#' .env | xargs) && flyway migrate -url=jdbc:postgresql://127.0.0.1:${POSTGRES_PORT}/${POSTGRES_DB} -user=${POSTGRES_USER} -password=${POSTGRES_PASSWORD} -locations="filesystem:./migrations" -baselineOnMigrate=true
```

Очистка базы данных:
```shell
export $(grep -v '^#' .env | xargs) && flyway clean -url=jdbc:postgresql://127.0.0.1:${POSTGRES_PORT}/${POSTGRES_DB} -user=${POSTGRES_USER} -password=${POSTGRES_PASSWORD} -locations="filesystem:./migrations" -cleanDisabled=false
```

#### ROLLBACK
Несмотря на то, что такой функционал имеется, использовать его в production плохая идея.
Например, если миграция добавляет столбцы, колонки, то undo их удаляет, что ведет к потере данных и обычно недопустимо.

Это не единственный минус rollback миграций, более подробно можно почитать [здесь.](https://flywaydb.org/documentation/concepts/migrations#important-notes)

Решение - писать roll-forward миграции, откат изменений происходит в миграциях "вверх".
