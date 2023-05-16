# Создание индекса
```
PUT localhost:41554/worker
```
```json
{
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    },
    "mappings": {
        "properties": {
            "f_name": {
                "type": "keyword"
            },
            "s_name": {
                "type": "keyword"
            },
            "age": {
                "type": "long"
            },
            "work_experience": {
                "type": "long"
            },
            "education": {
                "type": "keyword"
            },
            "info": {
                "type": "nested",
                "properties": {
                    "company": {
                    "type": "keyword"
                    },
                    "position": {
                    "type": "keyword"
                    },
                    "work_since": {
                    "type": "long"
                    }
                }
            },
            "achievements": {
                "type": "keyword"
            }
        }
    }
}
```
# Вставка данных
```b
POST localhost:41554/_bulk
```
```json
{"index":{"_index":"worker","_id":"Maddison"}}
{"f_name":"Thomas","s_name":"Maddison","age":20,"work_experience":0,"education":"University of Michigan, Masters degree","info":{"company":"Icing On The Cake","position":"intern","work_since":2022},"achievements":["Russian bear cub","School Biology Olympiad","All - Russian Olympiad of Schoolchildren","Thank you letter"]}
{"index":{"_index":"worker","_id":"Olbrighton"}}
{"f_name":"Alice","s_name":"Olbrighton","age":42,"work_experience":7,"education":"Duke University, Bachelors degree","info":{"company":"Icing On The Cake","position":"middle","work_since":2015},"achievements":["Russian bear cub","School Biology Olympiad"]}
{"index":{"_index":"worker","_id":"Tyler"}}
{"f_name":"Adam","s_name":"Tyler","age":33,"work_experience":5,"education":"College","info":{"company":"Herb","position":"middle","work_since":2017},"achievements":["All - Russian Olympiad of Schoolchildren","Thank you letter"]}
{"index":{"_index":"worker","_id":"Stones"}}
{"f_name":"Maria","s_name":"Stones","age":21,"work_experience":2,"education":"Yale University, Bachelors degree","info":[{"company":"Coppa-Coulla","position":"junior","work_since":2020},{"company":"South Wind","position":"junior","work_since":2020},{"company":"MooV","position":"junior","work_since":2021}],"achievements":["School Biology Olympiad","Thank you letter"]}
{"index":{"_index":"worker","_id":"Walker"}}
{"f_name":"Jeremy","s_name":"Walker","age":54,"work_experience":25,"education":"University of Michigan, Masters degree","info":[{"company":"Coppa-Coulla","position":"senior","work_since":1997},{"company":"Herb","position":"senior","work_since":1999}]}
{"index":{"_index":"worker","_id":"Bullet"}}
{"f_name":"Nick","s_name":"Bullet","age":65,"work_experience":19,"education":"School","info":[{"company":"Coppa-Coulla","position":"senior","work_since":2003},{"company":"Herb","position":"senior","work_since":2004}]}
{"index":{"_index":"worker","_id":"King"}}
{"f_name":"Antony","s_name":"King","age":27,"work_experience":4,"education":"Dartmouth College","info":[{"company":"Coppa-Coulla","position":"junior","work_since":2019},{"company":"Herb","position":"senior","work_since":2018}]}
{"index":{"_index":"worker","_id":"Swanson"}}
{"f_name":"Elizabeth","s_name":"Swanson","age":36,"work_experience":13,"education":"College","info":{"company":"South Wind","position":"middle","work_since":2009}}
{"index":{"_index":"worker","_id":"Sweet"}}
{"f_name":"Pol","s_name":"Sweet","age":48,"work_experience":8,"education":"School","info":{"company":"MooV","position":"middle","work_since":2014}}
{"index":{"_index":"worker","_id":"Stallman"}}
{"f_name":"Karolin","s_name":"Stallman","age":24,"work_experience":5,"education":"University of Miami, Masters degree","info":{"company":"MooV","position":"middle","work_since":2017}}

```
# Получение документа
```
GET localhost:41554/worker/_doc/Maddison
```
# Обновление документа
```
POST localhost:41554/worker/_update/Maddison
```
```json
{
    "doc": {
        "age": 21
    }
}
```
# Удаление документа
```
DELETE localhost:41554/worker/_doc/Maddison
```
# Удаление индекса
```
DELETE localhost:41554/worker
```