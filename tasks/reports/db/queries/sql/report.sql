-- name: get_calendar_statistics
WITH ranked AS (
	SELECT
	    s.date,
	    s.minutes,
	    ROW_NUMBER() OVER (PARTITION BY date ORDER BY s.created_dt DESC) AS rank
	FROM pt.statistics s
	JOIN pt.calendar c on s.calendar_id = c.id 
	WHERE 
	    c.name = :calendar_name
	    AND s.date between :start AND :end
),
dedublicated AS (
	SELECT 
		date,
		minutes
	FROM ranked 
	WHERE rank = 1
),
date_series AS (
	SELECT 
		generate_series(
			:start,
			:end,
			'1 day'
		) AS date
),
filled_empties AS (
	SELECT
		ds.date,
		coalesce(stat.minutes, 0) AS minutes
	FROM date_series ds
	LEFT JOIN dedublicated stat on ds.date = stat.date
)
SELECT 
	:calendar_name as calendar_name,
	date,
	minutes
FROM filled_empties;


-- name: get_user_calendars
SELECT
    name
FROM pt.calendar
WHERE 
    user_id = :user_id;