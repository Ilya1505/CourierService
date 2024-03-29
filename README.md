![Python](https://img.shields.io/badge/Python-3.11.5-_)
![FastApi](https://img.shields.io/badge/FastApi-0.108.0-orange)
![Alembic](https://img.shields.io/badge/Alembic-1.13.1-red)
![SqlAlchemy](https://img.shields.io/badge/SqlAlchemy-2.0.25-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13.3-blue)
![Docker](https://img.shields.io/badge/Docker-24.0.6-blue)


# Тестовое задание Courier Service от [*Estesis.tech*](https://estesis.tech)

Проект является REST API сервис для распределения заказов по курьерам.
Использованный стек: Python/FastAPI/SQLAlchemy.

Курьеры могут брать и завершать заказы. У курьера есть своя карточка с информацией: среднее выполнение заказа и среднее количество завершенных заказов в день. Курьер может выполнять максимум один заказ одновременно

## Реализованы следующие эндпоинты:

### 1) Регистрация курьера в системе.
```
POST /courier
```
Получаемые поля: 
+ name: str - имя курьера
+ districts: list[str] - массив районов.

У заказа и курьера должен быть общий район

### 2) Получение информации о всех курьеров системе.
```
GET /courier
```
Возвращаемые поля:
+ sid: UUID - уникальный идентификатор.
+ name: str - имя курьера

### 3) Получение подробной информации о курьере
```
GET /courier/{sid}
```
Возвращаемые поля:
+ sid: UUID - уникальный идентификатор.
+ name: str - имя курьера
+ active_order: dict - информация об активном заказе. Если такого нет, возвращается None
+ avg_order_complete_time: datetime - среднее время отработки заказа
+ avg_day_orders: int - среднее количество завершенных заказов в день

### 4) Публикация заказа в системе
```
4) POST /order
```
Получаемые поля:

+ name: str - имя заказа
+ district: str - район заказа.

В случае, если удалось найти подходящего курьера, запрос возвращает order_sid (id заказа) и courier_sid (id курьера).
Если подходящего курьера нет, то запрос возвращает ошибку.

### 5) Получение информации о заказе
```
GET /order/{sid}
```
Возвращаемые поля:

+ courier_sid: UUID
+ status: str - статус заказа. '1' - в работе, '2' - завершен

### 6) Завершение заказа
```
POST /order/{sid}
```

Возвращает ошибку если заказ уже завершен или такого заказа нет

### 7) Добавление района
```
POST /courier/create_district
```
Получаемые поля:
+ name: str - имя района

### 8) Получение списка всех районов
```
GET /courier/get_districts
```
Возвращаемые поля:
+ courier_sid: UUID
+ name: str - имя района


## Инструкция по запуску в Docker:

### 1) Установите [Docker](https://www.docker.com/)

### 2) Склонируйте репозиторий:

``` 
git clone https://github.com/Ilya1505/CourierService.git
```

### 3) Настройка файла .env
По умолчанию файл окружения [.env](.env) уже настроен и имеет рабочую конфигурацию,
но для исключения возможных ошибок запуска, рекомендуется проверить корректность 
указания хоста и сетевых портов под свою систему.

В случае редактировании **.env** будте аккуратны с ***хостами*** и ***портами***. 
Следите, чтобы они совпадали с соответствующими ***хостами*** и ***портами*** сервисов в [docker-compose.yaml](docker-compose.yaml).

Пример заполнения файла .env:
```
#Docker postgres
POSTGRES_DB=NAME_DB
POSTGRES_USER=USER_DB
POSTGRES_PASSWORD=PASSWORD_DB
POSTGRES_HOST=HOST_DB
POSTGRES_PORT=PORT_DB
```
### 4) Запуск Docker

Для сборки образов и запуска всех docker-контейнеров воспользуйтесь командами docker-compose:

+ Сборка образов:
  ```
  docker-compose build
  ```

+ Запуск всех контейнеров:
  ```
  docker-compose up -d
  ```

В случае возникновения ошибок, убедитесь, что имя хоста корректно
и указанные сетевые порты свободны в файлах [.env](.env) и
[docker-compose.yaml](docker-compose.yaml)

### 5) Заключение
После успешного выполнения вышеуказанных команд, запускаются два контейнера:

+ **postgres_db** - контейнер с базой данных postgres

+ **backend** - контейнер с реализованным функционалом сервиса CourierService 
