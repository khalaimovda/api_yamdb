# api_yamdb
## Проект предназначен для отработки навыков групповой разработки с участием трех человек.
## Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles)
## Использование проекта возможно только через API 

### Ознакомиться с полным функционалом и примерами можно по адресу http://127.0.0.1:8000/redoc Доступному после запуска проекта 
### Некоторые из примеров: 

### Получить список всех категорий
```
GET запрос: http://127.0.0.1:8000/api/v1/categories/
Ответ:
{
  "name": "string",
  "slug": "string"
}
```
### Получение всех произведений.
```
GET запрос: http://127.0.0.1:8000/api/v1/titles/
Ответ:
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной 
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

