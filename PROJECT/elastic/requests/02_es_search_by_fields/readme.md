# Поиск по соответствию
```
GET localhost:41554/worker/_search
```
```json
{
    "query": {
        "term": {
            "education": "College"
        }
    }
}
```
# Поиск по содержанию в массиве примитивных типов
```
GET localhost:41554/worker/_search
```
```json
{
    "query": {
        "term": {
            "achievements": "All - Russian Olympiad of Schoolchildren"
        }
    }
}
```
# Поиск по содержанию в массиве объектов
```
GET localhost:41554/worker/_search
```
```json
{
    "query": {
        "nested": {
            "path": "info",
            "query": {
                "term": {
                    "info.company": "Icing On The Cake"
                }
            }
        }
    }
}
```
# Поиск по диапазону
```
GET localhost:41554/worker/_search
```
```json
{
    "query": {
        "range": {
            "age": {
                "gte": 25,
                "lte": 50
            }
        }
    }
}
```
# Поиск по выражению
```
GET localhost:41554/worker/_search
```
```json
{
    "query": {
        "script": {
            "script": "doc['age'].value - doc['work_experience'].value < 25"
        }
    }
}
```
# Поиск по существованию свойства:
```
GET localhost:41554/worker/_search
```
```json
{
    "query": {
        "exists": {
            "field": "achievements"
        }
    }
}
```
# Оператор must
```
GET localhost:41554/worker/_search
```
```json
{
    "query": {
        "bool": {
            "must": [
                {
                    "nested": {
                        "path": "info",
                        "query": {
                            "term": {
                                "info.position": "middle"
                            }
                        }
                    }
                },
                {
                    "range": {
                        "age": {
                            "gt": 40
                        }
                    }
                }
            ]
        }
    }
}
```
# Оператор must not
```
GET localhost:41554/worker/_search
```
```json
{
    "query": {
        "bool": {
            "must_not": [
                {
                    "exists": {
                        "field": "achievements"
                    }
                }
            ]
         }
    }
}
```
# Оператор should
```
GET localhost:41554/worker/_search
```
```json
{
    "query": {
        "bool": {
            "should": [
                {
                    "term": {
                        "education": "College"
                    }
                },
                {
                   "term": {
                        "education": "School"
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }
}
```