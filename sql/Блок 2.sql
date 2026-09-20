--Множественные JOIN и проверка консистентности данных

--Контекст: 
--Таблица `ticket_flights` связывает `tickets` и `flights`, содержит поля `ticket_no`, `flight_id`, `fare_conditions`, `amount`. 
--Таблица `boarding_passes` содержит `ticket_no`, `flight_id`, `boarding_no`, `seat_no`.

/* Напишите запрос: вывести имена всех пассажиров, которые прошли регистрацию (есть boarding pass), 
 * но класс обслуживания `fare_conditions` равен ‘Business’, а также номер рейса (`flight_no`) и место. */
select t.passenger_name , f.flight_no , bp.seat_no 
from boarding_passes bp 
join tickets t 
	on t.ticket_no = bp.ticket_no
join flights f 
	on f.flight_id = bp.flight_id 
join ticket_flights tf 
	on tf.ticket_no = bp.ticket_no 
		and  tf.flight_id = bp.flight_id 
where tf.fare_conditions = 'Business';

--Напишите запрос, чтобы проверить консистентность данных: есть ли в таблице `tickets` «осиротевшие» билеты, для которых нет ни одной записи в `ticket_flights`. 
select t.ticket_no 
from tickets t 
left join ticket_flights tf 
	on tf.ticket_no = t.ticket_no 
where tf.flight_id is null;

--Напишите запрос: найти пассажиров, которые забронировали рейс, но не получили ни одного посадочного талона. 
--Выводить только случаи, где `flights.status = ‘Scheduled’`.
select t.passenger_name , tf.flight_id 
from flights f 
join ticket_flights tf 
	on tf.flight_id = f.flight_id 
join tickets t 
	on t.ticket_no = tf.ticket_no
left join boarding_passes bp 
	on bp.flight_id = tf.flight_id and bp.ticket_no = tf.ticket_no  
where bp.ticket_no  is null and f.status = 'Scheduled';



