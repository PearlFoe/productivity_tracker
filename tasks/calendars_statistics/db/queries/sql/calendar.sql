-- name: save_statistics
INSERT INTO pt.statistics (calendar_id, date, minutes)
VALUES (
    :calendar_id,
    :date,
    :minutes
);


-- name: get_calendars_to_parse
WITH calendars_with_daily_statistics AS (
    SELECT s.calendar_id
    FROM pt.statistics s
    WHERE s.date = :filter_date
)
SELECT
    c.id,
    c.name,
    c.description,
    c.google_id,
    c.timezone,
    cc.name AS category
FROM pt.calendar c
JOIN pt.calendar_category cc on c.category = cc.id
JOIN calendars_with_daily_statistics cds ON c.id = cds.calendar_id
WHERE 
    c.timezone = ANY(:timezones) AND
    cds.calendar_id IS NULL;