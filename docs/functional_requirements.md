## Функциональные Требования

1. **Управление пользователями:**
   - Регистрация и авторизация пользователей.
   - Управление личным профилем.

2. **Управление расписанием перелётов:**
   - Создание и обновление расписания перелётов.
   - Просмотр расписания перелётов.

3. **Управление бронями:**
   - Создание броней.
   - Изменение или удаление броней.

4. **Система услуг:**
   - Создание и изменение доступных услуг компании.
   - Создание заявок на услуги.

5. **Система отзывов:**
   - Возможность оставления отзывов о перелётах.
   - Просмотр оценок и отзывов.

6. **Управление вопросами и ответами:**
   - Создание вопросов для обсуждения.
   - Ответы на вопросы и изменение статуса.

7. **Управление акциями:**
   - Просмотр каталога возможных акций на услуги.
   - Создание и обновление акций на услуги.
   - Активация акций на услуги.

8. **Логирование действий:**
   - Запись действий системы для анализа работы компании.

## Сущности

### User
- `id`: UUID
- `role_id`: UUID
- `user_data_id`: UUID
- `login`: varchar
- `password`: varchar
- `name`: varchar
- `phone_number`: varchar
- `age`: int

### Role
- `id`: UUID
- `name`: varchar

### Service
- `id`: UUID
- `name`: varchar
- `price`: decimal

### Plane
- `id`: UUID
- `available_seats`: int
- `model`: varchar
- `company`: varchar

### Flight
- `id`: UUID
- `service_id`: UUID
- `origin_point`: varchar
- `destination_point`: varchar
- `departure_datetime`: timestamp
- `arrival_datetime`: timestamp
- `available_seats`: int
- `price`: decimal
- `is_active`: boolean
- `plane_id`: UUID

### Booking
- `id`: UUID
- `flight_id`: UUID
- `user_id`: UUID
- `seats_amount`: int
- `price`: int
- `datetime_created`: timestamp

### Promotions
- `id`: UUID
- `title`: varchar
- `description`: text
- `discount`: decimal
- `end_date`: date
- `service_id`: UUID

### Reviews
- `id`: UUID
- `text`: varchar
- `grade`: int
- `user_id`: UUID

### Questions
- `id`: UUID
- `user_id`: UUID
- `question`: varchar
- `answer`: varchar
- `status`: boolean

### ActionLog
- `id`: bigint
- `action`: varchar
- `datetime`: timestamp
- `user_id`: UUID




  Пассажир:
- Регистрация и авторизация пользователей
- Просмотр расписания перелётов
- Создание броней
- Изменение или удаление броней
- Создание заявок на услуги
- Возможность оставления отзывов о перелётах
- Просмотр оценок и отзывов
- Создание вопросов для обсуждения
- Просмотр каталога возможных акций на услуги


  Администратор:
- Регистрация и авторизация пользователей
- Создание и обновление расписания перелётов
- Просмотр расписания перелётов
- Изменение или удаление броней
- Создание и изменение доступных услуг компании
- Создание заявок на услуги
- Просмотр оценок и отзывов
- Ответы на вопросы и изменение статуса
- Просмотр каталога возможных акций на услуги
- Создание и обновление акций на услуги
- Активация акций на услуги

https://drawsql.app/teams/bsuir-24/diagrams/dbms