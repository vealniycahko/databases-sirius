```shell
curl --location --request GET 'http://localhost:47823/holders?limit=3&offset=1'
```

```shell
curl --location --request POST 'http://localhost:47823/holders/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Phone": "0010",
    "Name": "Иван Иванович"
}'
```
