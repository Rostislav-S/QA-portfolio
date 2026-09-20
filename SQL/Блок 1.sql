--Одиночные запросы и валидация данных

--Контекст: 
--Таблица bookings содержит поля book_ref (номер бронирования), book_date (дата бронирования), total_amount (общая сумма). 
--Таблица tickets содержит ticket_no, book_ref, passenger_id, passenger_name.

--Таблица bookings
--Найти все бронирования с суммой (`total_amount`) больше 100000, вернуть номер брони, дату бронирования и сумму, отсортировать по убыванию суммы.
select *
from bookings b 
where b.total_amount > 100000
order by b.total_amount desc;

--Нужно проверить, что «среди бронирований, созданных за последние 7 дней, нет записей с `total_amount`, равным NULL или 0». 
select *
from bookings b 
where b.book_date >= now() - interval '7 days'
	and (b.total_amount is null or b.total_amount = 0);

--Таблица Tickets
--Одним SQL-запросом посчитайте, сколько раз каждый пассажир (`passenger_id`) встречается в таблице `tickets`, 
--и выведите только тех пассажиров, у кого количество билетов больше 1, отсортировав по убыванию количества.
select t.passenger_id , count(t.passenger_id) as tickets_count
from tickets t 
group by t.passenger_id
having count(t.passenger_id) > 1
order by tickets_count desc;


