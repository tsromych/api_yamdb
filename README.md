# Документация YaMDb

## Описание

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство»). Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Добавлять произведения, категории и жанры может только администратор.

Авторизованные пользователи могут оставлять к произведениям текстовые отзывы и ставить оценку в диапазоне от одного до десяти, из пользовательских оценок формируется рейтинг произведения. Также пользователи могут оставлять комментарии к отзывам.

Для неавторизованных пользователей работа с API доступна только в режиме чтения.

## Стек технологий

* Python 3.9,
* Django 3.2,
* Django REST Framework 3.12,
* Simplejwt 4.7

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:tsromych/api_yamdb.git
```
```bash
cd api_yamdb
```

Cоздать виртуальное окружение:

```bash
# Для Windows
python -m venv venv

# Для MacOS, Linux
python3 -m venv env
```

Активировать виртуальное окружение:

```bash
# Для Windows
source venv/Scripts/activate

# Для MacOS, Linux
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
# Для Windows
python -m pip install --upgrade pip

# Для MacOS, Linux
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
cd api_yamdb
```
```bash
# Для Windows
python manage.py migrate

# Для MacOS, Linux
python3 manage.py migrate
```

Запустить проект:

```bash
# Для Windows
python manage.py runserver

# Для MacOS, Linux
python3 manage.py runserver
```

## Загрузка тестовых данных

В проекте API YaMDb в директории `/api_yamdb/static/data` подготовлены csv-файлы с тестовым контентом для ресурсов Users, Titles, Categories, Genres, Review и Comments. Для загрузки данных выполните в терминале management-команду:

```bash
# Для Windows
python manage.py import_csv_to_db

# Для MacOS, Linux
python3 manage.py import_csv_to_db
```

## Документация к API проекта:
### Ресурсы API YaMDb

* Ресурс auth: аутентификация.
* Ресурс users: пользователи.
* Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
* Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
* Ресурс genres: жанры произведений.
* Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
* Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Примеры работы с API

Регистрация пользователя

```bash
# Права доступа: для всех пользователей
# POST запрос
# /api/v1/auth/signup/
{
  "email": "user@example.com",
  "username": "string"
}

# Отправка confirmation_code на почту указанную а запросе
```
Получение JWT-токена
```bash
# Права доступа: для всех пользователей
# POST запрос
# /api/v1/auth/token/
{
  "username": "string",
  "confirmation_code": "string"
}

# Response
{
  "token": "string"
}
```
Получение списка всех пользователей
```bash
# Права доступа: администратор
# GET запрос
# /api/v1/users/

# Response
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "username": "string",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }
  ]
}
```
Добавление нового отзыва
```bash
# Права доступа: аутентифицированные пользователи
# POST запрос
# /api/v1/titles/{title_id}/reviews/
{
  "text": "string",
  "score": 5
}

# Response
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Удаление отзыва по id
```bash
# Права доступа: автор отзыва, модератор или администратор
# DELETE запрос
# /api/v1/titles/{title_id}/reviews/{review_id}/

# Удаление отзыва с id указанном в эндпоинте
```

### Для получения полной документации перейдите по ссылке:
```bash
http://127.0.0.1:8000/redoc
```

## Авторы

* [Роман Цуленков (Categories/Genres/Titles)](https://github.com/tsromych)
* [Евгений Смирнов (Auth/Users)](https://github.com/SmirnovEvgenii)
* [Артём Климов (Review/Comments)](https://github.com/Artem-Klimov)
