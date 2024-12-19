CREATE TABLE Role (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE MyUser (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID REFERENCES Role(id) ON DELETE SET NULL,
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15),
    age INT CHECK (age > 0),
    service_id UUID
);

CREATE TABLE Plane (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    available_seats INT CHECK (available_seats > 0),
    model VARCHAR(50) NOT NULL,
    company VARCHAR(50) NOT NULL
);

CREATE TABLE Service (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    MyUser_id UUID REFERENCES MyUser(id) ON DELETE SET NULL,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) CHECK (price >= 0)
);

CREATE TABLE Flight (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_id UUID REFERENCES Service(id) ON DELETE CASCADE,
    origin_point VARCHAR(100) NOT NULL,
    destination_point VARCHAR(100) NOT NULL,
    departure_datetime TIMESTAMP NOT NULL,
    arrival_datetime TIMESTAMP NOT NULL,
    price DECIMAL(10, 2) CHECK (price >= 0),
    is_active BOOLEAN DEFAULT TRUE,
    plane_id UUID REFERENCES Plane(id) ON DELETE SET NULL
);

CREATE TABLE Booking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flight_id UUID REFERENCES Flight(id) ON DELETE CASCADE,
    MyUser_id UUID REFERENCES MyUser(id) ON DELETE CASCADE,
    seats_amount INT CHECK (seats_amount > 0),
    price DECIMAL(10, 2) CHECK (price >= 0),
    datetime_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text VARCHAR(500),
    grade INT CHECK (grade BETWEEN 1 AND 5),
    MyUser_id UUID REFERENCES MyUser(id) ON DELETE CASCADE
);

CREATE TABLE Questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    MyUser_id UUID REFERENCES MyUser(id) ON DELETE CASCADE,
    question VARCHAR(500) NOT NULL,
    answer VARCHAR(500),
    status BOOLEAN DEFAULT FALSE
);

CREATE TABLE Promotions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    discount DECIMAL(5, 2) CHECK (discount BETWEEN 0 AND 100),
    end_date DATE NOT NULL,
    service_id UUID REFERENCES Service(id) ON DELETE CASCADE
);

CREATE TABLE ActionLog (
    id BIGSERIAL PRIMARY KEY,
    action VARCHAR(100) NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    MyUser_id UUID REFERENCES MyUser(id) ON DELETE SET NULL
);

CREATE TABLE MyUser_service (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    MyUser_id UUID REFERENCES MyUser(id) ON DELETE CASCADE,
    service_id UUID REFERENCES Service(id) ON DELETE CASCADE
);

CREATE INDEX idx_MyUser_login ON MyUser (login);
CREATE INDEX idx_flight_points ON Flight (origin_point, destination_point);
CREATE INDEX idx_flight_is_active ON Flight (is_active);
CREATE INDEX idx_reviews_MyUser ON Reviews (MyUser_id);
CREATE INDEX idx_booking_flight ON Booking (flight_id);
CREATE INDEX idx_promotions_service ON Promotions (service_id);






-- INSERTING TEST VALUES TO DATABASE
INSERT INTO Role (name) VALUES
('Admin'),
('Passenger');

INSERT INTO MyUser (role_id, login, password, name, phone_number, age) VALUES
((SELECT id FROM Role WHERE name = 'Admin'), 'admin', 'admin', 'Admin User', '1234567890', 35),
((SELECT id FROM Role WHERE name = 'Passenger'), 'passenger1', 'pass123', 'John Doe', '9876543210', 28);
INSERT INTO Plane (available_seats, model, company) VALUES
(180, 'Boeing 737', 'Boeing'),
(200, 'Airbus A320', 'Airbus');

INSERT INTO Service (MyUser_id, name, price) VALUES
((SELECT id FROM MyUser WHERE name = 'John Doe'), 'Wi-Fi', 10.00);

INSERT INTO Flight (service_id, origin_point, destination_point, departure_datetime, arrival_datetime, price, plane_id) VALUES
((SELECT id FROM Service WHERE name = 'Wi-Fi'), 'New York', 'London', '2024-11-25 10:00:00', '2024-11-25 18:00:00', 500.00,
 (SELECT id FROM Plane WHERE model = 'Boeing 737'));

INSERT INTO Flight (service_id, origin_point, destination_point, departure_datetime, arrival_datetime, price, plane_id) VALUES
((SELECT id FROM Service WHERE name = 'Wi-Fi'), 'London', 'New York', '2024-11-25 10:00:00', '2024-11-25 18:00:00', 600.00,
 (SELECT id FROM Plane WHERE model = 'Airbus A320'));

INSERT INTO Booking (flight_id, MyUser_id, seats_amount, price) VALUES
((SELECT id FROM Flight WHERE origin_point = 'London'), (SELECT id FROM MyUser WHERE login = 'passenger1'), 1, 500.00);

INSERT INTO Promotions (title, description, discount, end_date, service_id) VALUES
('Black Friday Sale', '50% off on Wi-Fi service', 50.00, '2024-12-30',
 (SELECT id FROM Service WHERE name = 'Wi-Fi'));

INSERT INTO Questions (MyUser_id, question) VALUES
((SELECT id from myuser where name = 'John Doe'), 'Самые дешевые направления');

-- Получить все активные рейсы
SELECT * FROM Flight WHERE is_active = TRUE;

-- Найти все бронирования пользователя
SELECT * FROM Booking WHERE MyUser_id = (SELECT id FROM MyUser WHERE login = 'passenger1');

-- Список услуг с акциями
SELECT s.name, p.title, p.discount
FROM Service s
JOIN Promotions p ON s.id = p.service_id;

-- Лог действий определенного пользователя
SELECT * FROM ActionLog WHERE MyUser_id = (SELECT id FROM MyUser WHERE login = 'admin');

-- Обновить статус вопроса
UPDATE Questions SET status = TRUE WHERE question = 'Какие самые дешёвые направления из Москвы?';

-- Удалить старые акции
DELETE FROM Promotions WHERE end_date < CURRENT_DATE;



SELECT DISTINCT age FROM MyUser
WHERE age BETWEEN 30 AND 40
ORDER BY age DESC;