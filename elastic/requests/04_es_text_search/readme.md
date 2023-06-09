# Создание индекса по словоформам и синонимам
```
PUT localhost:41554/company
```
```json
{
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "analysis": {
            "filter": {
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                },
                "my_synonym": {
                    "type": "synonym",
                    "synonyms": [
                        "coca-cola => кока-кола",
                        "coca-cola => кокакола",
                        "coca-cola => кола",
                        "coca-cola => cola",
                        "coca-cola => cocacola",
                        "moov => движение",
                        "moov => мув",
                        "herb => трава",
                        "herb => зелень",
                        "herb => растения",
                        "herb => grass",
                        "herb => plant",
                        "herb => greenery"
                    ]
                }
            },
            "analyzer": {
                "title_ru_analyzer": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "russian_stop",
                        "russian_stemmer",
                        "my_synonym"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "title_ru_analyzer"
            },
            "founded": {
                "type": "keyword"
            },
            "field": {
                "type": "keyword"
            }
        }
    }
}
```
# Вставка данных
```
GET localhost:41554/worker/_search
```
```json
{"index":{"_index":"company"}}
{"title": "Coca-Cola", "founded": "Январь, 1892", "field": "Напитки"}
{"index":{"_index":"company"}}
{"title": "Южный Ветер", "founded": "Апрель, 2007", "field": "Отели"}
{"index":{"_index":"company"}}
{"title": "MooV", "founded": "Сентябрь, 2000", "field": "Грузоперевозки"}
{"index":{"_index":"company"}}
{"title": "Вишенка", "founded": "Июль, 2013", "field": "Рестораны"}
{"index":{"_index":"company"}}
{"title": "Herb", "founded": "Декабрь, 1980", "field": "Фермы"}

```
# Поиск по словоформе
```
POST localhost:41554/_bulk
```
```json
{
    "query": {
        "match": {
            "title": {
                "query": "вишенкам",
                "analyzer": "title_ru_analyzer"
            }
        }
    }
}
```
# Поиск по синонимам
```
GET localhost:41554/company/_search
```
```json
{
    "query": {
        "match": {
            "title": {
                "query": "кола",
                "analyzer": "title_ru_analyzer"
            }
        }
    }
}
```
# Поиск по нечёткому соответствию
```
GET localhost:41554/worker/_search
```
```json
{
    "query": {
        "match": {
            "title": {
                "query": "южны ветир",
                "analyzer": "title_ru_analyzer",
                "fuzziness": 1
            }
        }
    }
}
```
# Удаление индекса
```
DELETE localhost:41554/company
```
# Создание edge n-gram индекса
```
PUT localhost:41554/company
```
```json
{
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "analysis": {
            "filter": {
                "title_ngram_filter": {
                    "type": "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 5
                }
            },
            "analyzer": {
                "title_ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "title_ngram_filter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "title_ngram_analyzer"
            },
            "founded": {
                "type": "keyword"
            },
            "field": {
                "type": "keyword"
            }
        }
    }
}
```
# Вставка данных
```
POST localhost:41554/_bulk
```
```json
{"index":{"_index":"company"}}
{"title": "Coca-Cola", "founded": "Январь, 1892", "field": "Напитки"}
{"index":{"_index":"company"}}
{"title": "Южный Ветер", "founded": "Апрель, 2007", "field": "Отели"}
{"index":{"_index":"company"}}
{"title": "MooV", "founded": "Сентябрь, 2000", "field": "Грузоперевозки"}
{"index":{"_index":"company"}}
{"title": "Вишенка", "founded": "Июль, 2013", "field": "Рестораны"}
{"index":{"_index":"company"}}
{"title": "Herb", "founded": "Декабрь, 1980", "field": "Фермы"}

```
# Поиск по началу слова 
```
GET localhost:41554/company/_search
```
```json
{
    "query": {
        "match": {
            "title": {
                "query": "co",
                "analyzer": "title_ngram_analyzer"
            }
        }
    }
}
```