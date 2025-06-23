# Currency API

Этот проект — REST API для работы с валютами. Реализованы эндпоинты для получения курсов валют, списка валют, регистрации и авторизации пользователей.

## Основные ручки API

### 1. Регистрация пользователя

``` POST /user/register/ ```

**Описание**: Регистрация нового пользователя.

**Тело запроса**: ```{"username": "string",  "password": "stringstri"}```

**Ответ**: Информация о созданном пользователе.

### 2. Вход пользователя (логин)

```POST /user/login/```

**Описание**: Аутентификация пользователя и получение токена.

**Тело запроса**: ```{"username": "string",  "password": "stringstri"} ```

**Ответ**: JSON с токеном доступа.

### 3. Получение курсов валют

```GET /currency/exchange/```

**Описание**: Возвращает текущие курсы указанных валют. Запрос возможен только после авторизации.

**Параметры запроса**:
+ ***currencies*** (строка, обязательный): список валют через запятую, например *USD,EUR,JPY*.
+ ***source*** (опционально): валюта, с которой сравниваются *currencies* (по умолчанию: USD).
+ ***count*** (опционально): количество *source* (по умолчанию: 1).

**Ответ**: JSON с курсами валют.

### 4. Получение списка доступных валют

```GET /currency/list/```

**Описание**: Возвращает список всех поддерживаемых валют. Запрос возможен только после авторизации.

**Ответ**: JSON со списком валют.

## Как запустить проект
* Клонируйте репозиторий:

``` git clone https://github.com/professorLumpen/currency_converter```

* Создайте виртуальное окружение и активируйте его:

```python -m venv venv```

```source venv/bin/activate   # Linux/MacOS```

```venv\Scripts\activate      # Windows ```
* Установите зависимости:

```pip install -r requirements.txt```
* Создайте файл .env и задайте переменные окружения:
  + DB_HOST=localhost
  + DB_PORT=5432
  + DB_USER=your_user
  + DB_PASS=your_password
  + DB_NAME=your_db_name
  + TEST_DB_NAME=your_test_db_name 
  + CURRENCY_API_KEY=your_api_key 
  + CURRENCY_API_URL=https://api.currency.com/
  + JWT_SECRET_KEY=your_secret_key 
  + JWT_ALGORITHM=HS256 
  + ACCESS_TOKEN_EXPIRE_MINUTES=30


* Запустите приложение
``` uvicorn main:app --reload ```


## Документация по использованию API
Вы можете использовать любой инструмент для тестирования API (Postman, curl).

### Примеры запросов:

#### Получение курсов валют: *(Сколько долларов и евро в 10 рублях)*

```
curl -X GET "http://localhost:8000/currency/exchange/?currencies=USD,EUR&source=RUB&count=10"
```


#### Регистрация пользователя:


```
curl -X POST "http://localhost:8000/user/register/" \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass12"}'
```

#### Логин и получение токена:
```
curl -X POST "http://localhost:8000/user/login/" \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass12"}'
```

### Важные замечания
+ Перед запуском убедитесь, что у вас настроена база данных и она запущена.
+ Для безопасности не храните секретные ключи в публичных репозиториях.
+ Для тестирования используйте отдельную тестовую базу данных.