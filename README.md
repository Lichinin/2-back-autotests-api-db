# 2.-Block-D.-Back-autotests-API-DB

**Автор:** Виталий Личинин  
**Репозиторий:** [GitHub](https://github.com/Lichinin/2-back-autotests-api-db)

## Оглавление
1. [Цели проекта](#цели-проекта)
2. [Технологии](#используемые-технологии)
3. [Структура проекта](#структура-проекта)
4. [Запуск тестов](#запуск-проекта)
5. [Настройка окружения](#настройка-env)
6. [Фикстуры](#фикстуры)
7. [Примеры логов тестов](#примеры-логов)
8. [Примеры отчетности Allure](#примеры-отчетности-allure)

---

## Цели проекта
- Автоматизация тестирования REST API
- Реализация клиента API
- Проверка данных в базе данных
- Интеграция Allure для отчетности
- Генерация тестовых данных с Faker
- Валидация схем ответа API
- Настройка pre-commit хуков для контроля качества кода

## Используемые технологии

| Компонент         | Версия    | Назначение                          |
|-------------------|-----------|-------------------------------------|
| python            | 3.10      | Базовый язык                        |
| pytest            | 8.3.5     | Фреймворк для тестирования          |
| requests          | 2.32.3    | HTTP-запросы к API                  |
| pydantic          | 2.11.1    | Валидация данных                    |
| allure-pytest     | 2.13.5    | Генерация отчетов Allure            |
| Faker             | 37.1.0    | Генерация тестовых данных           |
| flake8            | 7.2.0     | Линтер для проверки стиля кода      |
| mysql-connector   | 9.3.0     | Подключение к базе данных           |
| pre_commit        | 4.2.0     | Автоматизация проверок перед коммитом|
| python-dotenv     | 1.1.0     | Безопасное храниние данных          |


## Структура проекта

2-back-autotests-api-db                                                  
├─ allure-results                                                        
├─ api_client                                                            
│  ├─ api_client.py                                                      
│  └─ base_api_clint.py                                                  
├─ helpers                                                               
│  ├─ api_helpers.py                                                     
│  ├─ data_helpers.py                                                    
│  └─ db_helper.py                                                       
├─ log                                                                   
├─ schemas                                                               
│  └─ schemas.py                                                         
├─ tests                                                                 
│  ├─ test_api                                                           
│  │  └─ test_api.py                                                     
│  └─ conftest.py                                                        
├─ config.py                                                             
├─ pytest.ini                                                            
├─ README.md                                                             
└─ requirements.txt                                                      

### Описание папок
- **allure-results** -  результаты для генерации Allure-отчетов
- **api_client** - содержит реализацию клиента для работы с API
- **helpers** - вспомогательные функции для тестов
- **logs** - логи выполнения тестов (автогенерация) 
- **schemas** - модели данных для валидации ответов API
- **tests** - тестовые сценарии с использованием pytest

### Ключевые файлы
- **api_client.py** - основной клиент для работы с API
- **schemas.py** - модели Pydantic для валидации ответов
- **conftest.py** - фикстуры для управления тестовыми данными
- **data_helpers.py** - генератор тестовых данных

### Фикстуры

| Фикстура              | Назначение                                                            |
|-----------------------|-----------------------------------------------------------------------|
| configure_logging     | Настройка логирования                                                 |
| api_client            | Создание клиента для взаимодействия с API                             |
| setup_post            | Создание одного или нескольких постов с последующей очисткой          |
| db_connection         | Соединение с базой данных через DatabaseHelper                        |
| posts_to_delete_list  | Добавляет созданные посты в список для удаления после теста           |
| created_post          | Создаёт один пост и возвращает его данные                             |
| users_to_delete_list  | Добавляет созданных пользователей в список для удаления после теста   |
| created_user          | Создаёт одного пользователя и возвращает его данные                   |
| setup_user            | Создаёт одного или несколько пользователей с очисткой после теста     |


## Запуск проекта

### Установка зависимостей
```bash
git clone https://github.com/Lichinin/2-back-autotests-api-db
cd 2-back-autotests-api-db
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```
**Настройка env**
В корне проекта создайте файл `.env` и заполните его следующими данными:

```
DB_HOST=localhost
DB_USER=wordpress
DB_PASSWORD=wordpress
DB_NAME=wordpress
DB_PORT=3306
USERNAME=`логин администратора`
PASSWORD=`пароль администратора`
BASE_URL=http://localhost:8000

```
**Запуск**
```
pytest
```


### Примеры логов.
***test_create_comment.log***
```
2025-05-30 18:07:08,728 - test_create_comment - INFO - Test started: test_create_comment
2025-05-30 18:07:08,728 - fixture.api_client - INFO - ====> Fixture ApiClient started
2025-05-30 18:07:08,729 - fixture.setup_post - INFO - ====> Fixture setup started
2025-05-30 18:07:08,730 - fixture.setup_post - INFO - ====> Fixture: Try create post for test
2025-05-30 18:07:08,732 - ApiClient - INFO - Send POST request to http://localhost:8000/wp-json/wp/v2/posts
2025-05-30 18:07:08,924 - fixture.setup_post - INFO - ====> Fixture: Successful create post (id=272) for test.
2025-05-30 18:07:08,925 - fixture.db_connection - INFO - ====> Connect to database
2025-05-30 18:07:08,982 - ApiClient - INFO - Send POST request to http://localhost:8000/wp-json/wp/v2/comments
2025-05-30 18:07:09,142 - validation.CommentModel - INFO - * Check response scheme
2025-05-30 18:07:09,143 - validation.CommentModel - INFO - entity data: {'id': 101, 'post': 272, 'parent': 0, 'author': 0, 'author_name': 'Behind dark another body we whose leg general.', 'author_email': 'mgraham@example.org', 'author_url': '', 'author_ip': '172.18.0.1', 'author_user_agent': 'python-requests/2.32.3', 'date': '2025-05-30T18:07:09', 'date_gmt': '2025-05-30T15:07:09', 'content': {'rendered': '<p>Join adult might describe explain kitchen once buy.</p>\n', 'raw': 'Join adult might describe explain kitchen once buy.'}, 'link': 'http://localhost:8000/beautiful-mr-including/#comment-101', 'status': 'approved', 'type': 'comment', 'author_avatar_urls': {'24': 'https://secure.gravatar.com/avatar/1b32d72f7372ecd42407dd20a540e105b5c78f1f240f320b9ef58b7de6cb6500?s=24&d=mm&r=g', '48': 'https://secure.gravatar.com/avatar/1b32d72f7372ecd42407dd20a540e105b5c78f1f240f320b9ef58b7de6cb6500?s=48&d=mm&r=g', '96': 'https://secure.gravatar.com/avatar/1b32d72f7372ecd42407dd20a540e105b5c78f1f240f320b9ef58b7de6cb6500?s=96&d=mm&r=g'}, 'meta': [], '_links': {'self': [{'href': 'http://localhost:8000/wp-json/wp/v2/comments/101', 'targetHints': {'allow': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']}}], 'collection': [{'href': 'http://localhost:8000/wp-json/wp/v2/comments'}], 'up': [{'embeddable': True, 'post_type': 'post', 'href': 'http://localhost:8000/wp-json/wp/v2/posts/272'}]}}
2025-05-30 18:07:09,144 - validation.CommentModel - INFO - * Scheme is valid.
2025-05-30 18:07:09,144 - Get comment form database - INFO - * Execute query
2025-05-30 18:07:09,151 - Get comment form database - INFO - * Assert 101 == 101
2025-05-30 18:07:09,151 - Get comment form database - INFO - * Assert Behind dark another body we whose leg general. == Behind dark another body we whose leg general.
2025-05-30 18:07:09,152 - Get comment form database - INFO - * Assert Join adult might describe explain kitchen once buy. == Join adult might describe explain kitchen once buy.
2025-05-30 18:07:09,160 - fixture.setup_post - INFO - ====> Fixture: Delete post (id=272) for test
2025-05-30 18:07:09,161 - ApiClient - INFO - Send DELETE request to http://localhost:8000/wp-json/wp/v2/posts/272?force=true
2025-05-30 18:07:09,359 - fixture.setup_post - INFO - ====> Fixture setup exit
2025-05-30 18:07:09,366 - fixture.api_client - INFO - ====> Fixture ApiClient teardown
2025-05-30 18:07:09,368 - test_create_comment - INFO - Test finished: test_create_comment
```

**test_get_post_by_id.log**
```
2025-05-30 18:07:17,732 - test_get_post_by_id - INFO - Test started: test_get_post_by_id
2025-05-30 18:07:17,733 - fixture.api_client - INFO - ====> Fixture ApiClient started
2025-05-30 18:07:17,734 - fixture.setup_post - INFO - ====> Fixture setup started
2025-05-30 18:07:17,734 - fixture.setup_post - INFO - ====> Fixture: Try create post for test
2025-05-30 18:07:17,736 - ApiClient - INFO - Send POST request to http://localhost:8000/wp-json/wp/v2/posts
2025-05-30 18:07:17,928 - fixture.setup_post - INFO - ====> Fixture: Successful create post (id=278) for test.
2025-05-30 18:07:17,931 - ApiClient - INFO - Send GET request to http://localhost:8000/wp-json/wp/v2/posts/278
2025-05-30 18:07:18,054 - validation.PostModel - INFO - * Check response scheme
2025-05-30 18:07:18,055 - validation.PostModel - INFO - entity data: {'id': 278, 'date': '2025-05-30T18:07:17', 'date_gmt': '2025-05-30T15:07:17', 'guid': {'rendered': 'http://localhost:8000/subject-hospital-nation-least-ever-public-alone/'}, 'modified': '2025-05-30T18:07:17', 'modified_gmt': '2025-05-30T15:07:17', 'slug': 'subject-hospital-nation-least-ever-public-alone', 'status': 'publish', 'type': 'post', 'link': 'http://localhost:8000/subject-hospital-nation-least-ever-public-alone/', 'title': {'rendered': 'Subject hospital nation least ever public alone.'}, 'content': {'rendered': '<p>Commercial people run benefit might.</p>\n', 'protected': False}, 'excerpt': {'rendered': '<p>Commercial people run benefit might.</p>\n', 'protected': False}, 'author': 1, 'featured_media': 0, 'comment_status': 'open', 'ping_status': 'open', 'sticky': False, 'template': '', 'format': 'standard', 'meta': {'footnotes': ''}, 'categories': [1], 'tags': [], 'class_list': ['post-278', 'post', 'type-post', 'status-publish', 'format-standard', 'hentry', 'category-1'], '_links': {'self': [{'href': 'http://localhost:8000/wp-json/wp/v2/posts/278', 'targetHints': {'allow': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']}}], 'collection': [{'href': 'http://localhost:8000/wp-json/wp/v2/posts'}], 'about': [{'href': 'http://localhost:8000/wp-json/wp/v2/types/post'}], 'author': [{'embeddable': True, 'href': 'http://localhost:8000/wp-json/wp/v2/users/1'}], 'replies': [{'embeddable': True, 'href': 'http://localhost:8000/wp-json/wp/v2/comments?post=278'}], 'version-history': [{'count': 0, 'href': 'http://localhost:8000/wp-json/wp/v2/posts/278/revisions'}], 'wp:attachment': [{'href': 'http://localhost:8000/wp-json/wp/v2/media?parent=278'}], 'wp:term': [{'taxonomy': 'category', 'embeddable': True, 'href': 'http://localhost:8000/wp-json/wp/v2/categories?post=278'}, {'taxonomy': 'post_tag', 'embeddable': True, 'href': 'http://localhost:8000/wp-json/wp/v2/tags?post=278'}], 'curies': [{'name': 'wp', 'href': 'https://api.w.org/{rel}', 'templated': True}]}}
2025-05-30 18:07:18,055 - validation.PostModel - INFO - * Scheme is valid.
2025-05-30 18:07:18,059 - fixture.setup_post - INFO - ====> Fixture: Delete post (id=278) for test
2025-05-30 18:07:18,061 - ApiClient - INFO - Send DELETE request to http://localhost:8000/wp-json/wp/v2/posts/278?force=true
2025-05-30 18:07:18,233 - fixture.setup_post - INFO - ====> Fixture setup exit
2025-05-30 18:07:18,239 - fixture.api_client - INFO - ====> Fixture ApiClient teardown
2025-05-30 18:07:18,241 - test_get_post_by_id - INFO - Test finished: test_get_post_by_id
```

### Примеры отчетности Allure.

Для просмотра отчетов:
```
allure serve allure-results
```
* Summary по тестам:
![image](https://github.com/user-attachments/assets/a9f43eb5-0f20-4995-9381-76faffe099c5)

* Тесткейсы:
![image](https://github.com/user-attachments/assets/448600b9-8833-4e58-bbed-d013537d6359)

* Пример отчета по тесткейсу:
![image](https://github.com/user-attachments/assets/20760773-2916-426b-ad17-c57680d6138d)
