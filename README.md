# YaMDb 

### Описание 

Проект YaMDb призван помочь отработать навыки групповой разработки с участием трех человек.
Проект реализует REST API для работы с отзывами на различные произведения искусства.
API позволяет: 
- Регистрировать пользователя с различными ролями (пользователь, модератор, администратор)
- Выполнять аутентификацию с помощью JWT
- Просматривать, создавать, редактировать и удалять произведения
- Просматривать, создавать и удалять жанры и категории произведений
- Просматривать, создавать, редактировать и удалять отзывы на произведения
- Просматривать, создавать, редактировать и удалять комментарии к отзывам
- Просматривать, создавать, редактировать и удалять пользвателей (администратор)

### Запуск проекта в dev-режиме (Windows) 

Клонировать GitHub-репозиторийи : 
``` 
git clone https://github.com/khalaimovda/api_yamdb.git
``` 

Перейти в директорию проекта:
``` 
cd api_yamdb
``` 

Cоздать и активировать виртуальное окружение: 
``` 
python -m venv venv 
source venv/Scripts/activate 
``` 

Установить необходимые инструменты из файла зависимостей: 
``` 
pip install -r requirements.txt 
``` 

Перейти в директорию основного приложения: 
``` 
cd api_yamdb 
``` 

Выполнить миграции: 
``` 
python manage.py migrate 
``` 

Заполнить БД тестовыми данными (опционально)
``` 
python manage.py filldb 
``` 

Запустить проект: 
``` 
python manage.py runserver 
``` 

### Регистрация нового пользователя 
Для регистрации нового пользователя необходимо выполнить запрос:
``` 
POST /api/v1/auth/signup/ 
{ 
    "email": "example@example.com"
    "username": "my_username", 
} 
``` 
На указанную почту придет код подтверждения, который нужно будет использовать для получения JWT (см. следующий шаг).

### Аутентификация 
Аутентификация на ресурсе происходит посредством JWT. Для его получения необходимо выполнить запрос: 
``` 
POST /api/v1/auth/token/  
{ 
    "username": "my_username", 
    "confirmation_code": "my_confirmation_code"" 
} 
``` 
В поле "confirmation_code" нужно передать, код полученный при регистрации пользователя (см. предыдущий шаг)

Ответ будет выглядеть примерно так: 
``` 
{ 
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMjE1OTU2OSwianRpIjoiNWZlNjUxNjEyMDFmNDIwYjg3Y2YxMTIwYjliNzNkMzUiLCJ1c2VyX2lkIjoxfQ.Ugsfl2RUAsIYSnErd4ubDaOLhmCm3yQ3paik90OvQFI"
} 
``` 
Все последующие запросы к ресурсу, требующие аутентификации, отправлять с заголовком 
``` 
Authorization: Bearer token
``` 

### Пример запроса к API 

Добавить новый отзыв "Текст отзыва" к произведению с id = 1, проставить произведению оценку 7 из 10:
``` 
POST /api/v1/titles/1/reviews/

Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMjE1OTU2OSwianRpIjoiNWZlNjUxNjEyMDFmNDIwYjg3Y2YxMTIwYjliNzNkMzUiLCJ1c2VyX2lkIjoxfQ.Ugsfl2RUAsIYSnErd4ubDaOLhmCm3yQ3paik90OvQFI

{ 
    "text": "Текст отзыва", 
    "score":  7
} 
``` 

**Более подробную документацию API смотрите на** 
``` 
/redoc/
/swagger/ 
``` 

### Авторы 
- Дмитрий Халаимов
- Роман Гербер
- Алексей Положенцев
