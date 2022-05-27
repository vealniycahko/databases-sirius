В данном примере есть 4 api метода, curl запросы которые им соответствуют:

### 1. Получение владельцев
```
curl --location --request GET 'http://localhost:8080/holders?offset=1&limit=2'
```

### 2. Добавление действия пользователя:
```
curl --location --request POST 'http://localhost:8080/user_actions?name=ivan&action=add_rectangle'
```
### 3. Отмена действия пользователя:
```
curl --location --request DELETE 'http://localhost:8080/user_actions?name=ivan'
```
### 4. Просмотр действий пользователя:
```
curl --location --request GET 'http://localhost:8080/user_actions?name=ivan'
```
