# Аггрегация
```
GET localhost:41554/worker/_search
```
```json
{
    "aggs": {
        "max_age": {
            "max": {
                "field": "age"
            }
        },
        "min_age": {
            "min": {
                "field": "age"
            }
        },
        "avg_age": {
            "avg": {
                "field": "age"
            }
        },
        "total_age": {
            "sum": {
                "script": "return doc['age'].value"
            }
        },
        "age_extended_stats": {
            "extended_stats": {
                "field": "age"
            }
        }
    },
    "size": 0
}
```
# Аггрегация с группироовкой по полю типа keyword
```
GET localhost:41554/worker/_search
```
```json
{
    "aggs": {
        "by_type": {
            "terms": {
                "field": "education"
            },
            "aggs": {
                "max_age": {
                    "max": {
                        "field": "age"
                    }
                },
                "min_age": {
                    "min": {
                        "field": "age"
                    }
                },
                "avg_age": {
                    "avg": {
                        "field": "age"
                    }
                },
                "total_age": {
                    "sum": {
                        "script": "return doc['age'].value"
                    }
                }
            }
        }
    },
    "size": 0
}
```
# Гистограмма
```
GET localhost:41554/worker/_search
```
```json
{
    "aggs": {
        "by_price": {
            "histogram": {
                "field": "age",
                "interval": 10
            },
            "aggs": {
                "avg_experience": {
                    "avg": {
                        "field": "work_experience"
                    }
                }
            }
        }
    },
    "size": 0
}
```