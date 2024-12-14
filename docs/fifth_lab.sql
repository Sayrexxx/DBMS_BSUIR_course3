CREATE OR REPLACE FUNCTION log_user_actions_func()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO ActionLog (action, datetime, myuser_id)
    VALUES (
        CASE
            WHEN TG_OP = 'INSERT' THEN 'Insert'
            WHEN TG_OP = 'UPDATE' THEN 'Update'
            WHEN TG_OP = 'DELETE' THEN 'Delete'
        END,
        CURRENT_TIMESTAMP,
        COALESCE(NEW.id, OLD.id)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_user_actions
AFTER INSERT OR UPDATE OR DELETE
ON MyUser
FOR EACH ROW
EXECUTE FUNCTION log_user_actions_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION check_seat_availability_func()
RETURNS TRIGGER AS $$
DECLARE
    available_seats INT;
BEGIN
    SELECT p.available_seats
    INTO available_seats
    FROM Plane p
    INNER JOIN Flight f ON f.plane_id = p.id
    WHERE f.id = NEW.flight_id;

    IF available_seats < NEW.seats_amount THEN
        RAISE EXCEPTION 'Not enough available seats for this booking.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER check_seat_availability
BEFORE INSERT
ON Booking
FOR EACH ROW
EXECUTE FUNCTION check_seat_availability_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_seats_after_booking_func()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Plane
    SET available_seats = available_seats - NEW.seats_amount
    WHERE id = (
        SELECT plane_id
        FROM Flight
        WHERE id = NEW.flight_id
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_seats_after_booking
AFTER INSERT
ON Booking
FOR EACH ROW
EXECUTE FUNCTION update_seats_after_booking_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_service_price_on_promotion_func()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Service
    SET price = price * (1 - NEW.discount)
    WHERE id = NEW.service_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_service_price_on_promotion
AFTER INSERT OR UPDATE
ON Promotions
FOR EACH ROW
EXECUTE FUNCTION update_service_price_on_promotion_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_expired_promotions_func()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM Promotions
    WHERE end_date < CURRENT_DATE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER delete_expired_promotions
AFTER INSERT OR UPDATE
ON Promotions
FOR EACH ROW
EXECUTE FUNCTION delete_expired_promotions_func();
------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_service_rating_func()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Service
    SET price = (
        SELECT AVG(grade)
        FROM Reviews
        WHERE myuser_id IN (
            SELECT myuser_id
            FROM myuser_service
            WHERE service_id = Service.id
        )
    )
    WHERE id IN (
        SELECT service_id
        FROM myuser_service
        WHERE myuser_id = NEW.myuser_id
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_service_rating
AFTER INSERT
ON Reviews
FOR EACH ROW
EXECUTE FUNCTION update_service_rating_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION check_flight_date_func()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.departure_datetime <= CURRENT_TIMESTAMP THEN
        RAISE EXCEPTION 'Departure date must be in the future.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER check_flight_date
BEFORE INSERT OR UPDATE
ON Flight
FOR EACH ROW
EXECUTE FUNCTION check_flight_date_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_question_status_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Если поле answer не пустое, устанавливаем статус TRUE
    IF NEW.answer IS NOT NULL AND NEW.answer <> '' THEN
        NEW.status := TRUE;
    ELSE
        -- Если поле answer пустое, устанавливаем статус FALSE
        NEW.status := FALSE;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;




CREATE TRIGGER update_question_status
BEFORE INSERT OR UPDATE
ON Questions
FOR EACH ROW
EXECUTE FUNCTION update_question_status_func();

------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validate_plane_seats_func()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.available_seats > 300 THEN
        RAISE EXCEPTION 'A plane cannot have more than 300 seats.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER validate_plane_seats
BEFORE INSERT OR UPDATE
ON Plane
FOR EACH ROW
EXECUTE FUNCTION validate_plane_seats_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION log_booking_creation_func()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO ActionLog (action, datetime, myuser_id)
    VALUES ('Booking created', CURRENT_TIMESTAMP, NEW.myuser_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER log_booking_creation
AFTER INSERT
ON Booking
FOR EACH ROW
EXECUTE FUNCTION log_booking_creation_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validate_unique_login_func()
RETURNS TRIGGER AS $$
DECLARE
    login_count INT;
BEGIN
    SELECT COUNT(*) INTO login_count
    FROM MyUser
    WHERE login = NEW.login;

    IF login_count > 0 THEN
        RAISE EXCEPTION 'Login already exists. Please choose a different login.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER validate_unique_login
BEFORE INSERT
ON MyUser
FOR EACH ROW
EXECUTE FUNCTION validate_unique_login_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_flight_status_func()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.arrival_datetime < CURRENT_TIMESTAMP THEN
        NEW.is_active = FALSE;
    ELSE
        NEW.is_active = TRUE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_flight_status
BEFORE INSERT OR UPDATE
ON Flight
FOR EACH ROW
EXECUTE FUNCTION update_flight_status_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION cleanup_old_logs_func()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM ActionLog
    WHERE datetime < CURRENT_TIMESTAMP - INTERVAL '90 days';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER cleanup_old_logs
AFTER INSERT
ON ActionLog
FOR EACH ROW
EXECUTE FUNCTION cleanup_old_logs_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validate_promotion_discount_func()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.discount <= 0 OR NEW.discount >= 100 THEN
        RAISE EXCEPTION 'Discount must be between 0 and 100.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER validate_promotion_discount
BEFORE INSERT OR UPDATE
ON Promotions
FOR EACH ROW
EXECUTE FUNCTION validate_promotion_discount_func();
------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validate_user_age_func()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.age < 18 THEN
        RAISE EXCEPTION 'User must be at least 18 years old.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Check trigger for logging user actions
CREATE TRIGGER validate_user_age
BEFORE INSERT OR UPDATE
ON MyUser
FOR EACH ROW
EXECUTE FUNCTION validate_user_age_func();






-- Examples for testing triggers:


INSERT INTO MyUser (id, role_id, login, password, name, phone_number, age)
VALUES (gen_random_uuid(), (SELECT id
                            FROM role
                            WHERE name='Passenger'), 'user1', 'password123', 'John Doe', '1234567890', 30);

UPDATE MyUser
SET name = 'Jane Doe', phone_number = '0987654321'
WHERE login = 'user1';

DELETE FROM MyUser
WHERE login = 'user1';

SELECT * FROM ActionLog;

--
INSERT INTO Booking (id, flight_id, myuser_id, seats_amount, price, datetime_created)
VALUES (gen_random_uuid(), '3e64a0b0-4b16-4393-8017-77d145afa631', '449f21bf-103c-4d12-a4fb-7ad4bac24f11', 3, 450.00, CURRENT_TIMESTAMP);

SELECT available_seats
FROM Plane
WHERE id = (SELECT plane_id FROM Flight WHERE id = '3e64a0b0-4b16-4393-8017-77d145afa631');
--

-- Promotions
INSERT INTO Promotions (id, title, description, discount, end_date, service_id)
VALUES (gen_random_uuid(), 'Black Friday Sale', 'Up to 50% off!', -10.00, '2024-12-31', (SELECT id
                                                                                                                            FROM service
                                                                                                                            WHERE name = 'Wi-Fi'));

INSERT INTO Promotions (id, title, description, discount, end_date, service_id)
VALUES (gen_random_uuid(), 'Holiday Sale', 'Save up to 30%!', 30, '2024-12-31', (SELECT id
                                                                                                                            FROM service
                                                                                                                            WHERE name = 'Wi-Fi'));
SELECT * FROM promotions;

--Check trigger for changing question status
UPDATE Questions
SET status = TRUE
WHERE myuser_id = (SELECT id
                   FROM myuser
                   WHERE name='');

SELECT * FROM ActionLog
WHERE action = 'Update';

--Check trigger for changing flight price
UPDATE Flight
SET price = price + 50
WHERE id = (SELECT id
            FROM flight
            WHERE origin_point ILIKE 'London');

SELECT * FROM ActionLog;

-- Check trigger for changing service price

--     //REMAKE//
UPDATE Service
SET price = price * 1.10
WHERE id = (SELECT id
            FROM Service
            WHERE name = 'Lounge Access');

SELECT * FROM ActionLog
WHERE action = 'Service Price Updated';

-- Check trigger for changing booking properties
UPDATE Booking
SET seats_amount = 4
WHERE id = 'ca15411e-3fea-4642-9136-5e8ec7a5ec5d';

-- Check trigger for logging plane details changing
UPDATE Plane
SET model = 'Boeing 737 Max'
WHERE company = 'Boeing';

-- Check trigger for not valid properties of Service entity
UPDATE Service
SET price = -50.00
WHERE id = (SELECT id
            FROM Service
            WHERE name = 'Lounge Access');

UPDATE Service
SET price = 200.00
WHERE name = 'Lounge Access';