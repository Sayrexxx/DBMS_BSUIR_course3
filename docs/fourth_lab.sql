SELECT f.origin_point, f.destination_point, f.departure_datetime, p.model, u.name AS user_name
FROM Flight f
JOIN Plane p ON f.plane_id = p.id
JOIN MyUser u ON f.service_id = (SELECT service_id FROM Service WHERE MyUser_id = u.id)
WHERE f.is_active = TRUE AND p.available_seats > 100 AND f.price < 300.00;

SELECT name, age
FROM MyUser
WHERE id IN (
    SELECT MyUser_id
    FROM Booking
    WHERE flight_id IN (
        SELECT id
        FROM Flight
        WHERE destination_point = 'New York'
    )
);



SELECT b.seats_amount, f.origin_point, f.destination_point, u.name AS passenger_name
FROM Booking b
INNER JOIN Flight f ON b.flight_id = f.id
INNER JOIN MyUser u ON b.MyUser_id = u.id
WHERE f.is_active = TRUE;


SELECT u.name, q.question, q.answer
FROM MyUser u
LEFT JOIN Questions q ON u.id = q.MyUser_id;


SELECT f.origin_point, f.destination_point, p.title, p.discount
FROM Flight f
FULL OUTER JOIN Promotions p ON f.service_id = p.service_id;


SELECT p.title AS promotion_title, f.origin_point, f.destination_point
FROM Promotions p
CROSS JOIN Flight f
WHERE p.end_date > CURRENT_DATE;


SELECT u1.name AS user1, u2.name AS user2
FROM MyUser u1
JOIN MyUser u2 ON u1.role_id = u2.role_id
WHERE u1.id != u2.id;



SELECT f.origin_point, COUNT(*) AS total_flights
FROM Flight f
GROUP BY f.origin_point
HAVING COUNT(*) > 5;


SELECT f.origin_point, f.destination_point, f.price,
       RANK() OVER (PARTITION BY f.origin_point ORDER BY f.price ASC) AS rank_by_price
FROM Flight f;


SELECT u.role_id, AVG(u.age) AS avg_age
FROM MyUser u
GROUP BY u.role_id
HAVING AVG(u.age) > 30;


SELECT f.origin_point, f.destination_point
FROM Flight f
WHERE departure_datetime > CURRENT_DATE
UNION
SELECT origin_point, destination_point
FROM Flight
WHERE arrival_datetime < CURRENT_DATE;



SELECT name
FROM MyUser u
WHERE EXISTS (
    SELECT 1
    FROM Booking b
    WHERE b.MyUser_id = u.id
);


INSERT INTO Reviews (text, grade, MyUser_id)
SELECT 'Отличный сервис', 5, MyUser_id
FROM Booking
WHERE price > 300.00;


SELECT f.origin_point, f.destination_point,
       CASE
           WHEN f.price < 300 THEN 'Дешево'
           WHEN f.price BETWEEN 300 AND 500 THEN 'Средняя цена'
           ELSE 'Дорого'
       END AS price_category
FROM Flight f;


EXPLAIN ANALYZE
SELECT *
FROM Booking b
JOIN Flight f ON b.flight_id = f.id
WHERE f.is_active = TRUE;
