## Функциональные Требования

1. **Управление пользователями:**
   - Регистрация и авторизация пользователей (Пассажир, Администратор).
   - Управление личным профилем.

2. **Управление расписанием перелётов:**
   - Создание и обновление расписания перелётов (Администратор).
   - Просмотр расписания перелётов (Пассажир, Администратор).

3. **Управление бронями:**
   - Создание броней (Пассажир).
   - Изменение или удаление броней (Пассажир, Администратор).

4. **Система услуг:**
   - Создание и изменение доступных услуг компании (Администратор).
   - Создание заявок на услуги (Пассажир, Администратор).

5. **Система отзывов:**
   - Возможность оставления отзывов о перелётах (Пассажир).
   - Просмотр оценок и отзывов (Пассажир, Администратор).

6. **Управление вопросами и ответами:**
   - Создание вопросов для обсуждения (Пассажир).
   - Ответы на вопросы и изменение статуса (Администратор).

7. **Управление акциями:**
   - Просмотр каталога возможных акций на услуги (Пассажир, Администратор).
   - Создание и обновление акций на услуги (Администратор).
   - Активация акций на услуги (Администратор).

8. **Логирование действий:**
   - Запись действий системы для анализа работы компании.

## Сущности

### User
- `id`: UUID
- `login`: varchar
- `password`: varchar
- `role_id`: uuid
- `user_data_id`: UUID

### UserData
- `id`: UUID
- `user_id`: UUID
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

https://drawsql.app/teams/bsuir-24/diagrams/dbms