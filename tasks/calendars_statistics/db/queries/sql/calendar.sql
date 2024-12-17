-- name: save_statistics
INSERT INTO pt.statistics (calendar_id, date, minutes)
VALUES (
    :calendar_id,
    :date,
    :minutes
);


-- name: get_calendars_by_timezone
SELECT
    c.id,
    c.name,
    c.description,
    c.google_id,
    c.timezone,
    cc.name as category
FROM pt.calendar c
JOIN pt.calendar_category as cc on c.category = cc.id
WHERE 
    c.timezone = ANY(:timezones);