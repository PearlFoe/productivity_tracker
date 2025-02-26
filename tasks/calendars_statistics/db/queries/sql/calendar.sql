-- name: save_statistics
INSERT INTO pt.statistics (calendar_id, date, minutes)
VALUES (
    :calendar_id,
    :date,
    :minutes
);


-- name: get_calendars_to_parse
WITH calendars_with_daily_statistics AS (
    SELECT DISTINCT s.calendar_id
    FROM pt.statistics s
    WHERE s.date = :filter_date
)
SELECT
    c.id,
    c.user_id,
    c.name,
    c.description,
    c.google_id,
    c.timezone,
    cc.name AS category
FROM pt.calendar c
JOIN pt.calendar_category cc ON c.category = cc.id
LEFT JOIN calendars_with_daily_statistics cds ON c.id = cds.calendar_id
WHERE 
    c.timezone = ANY(:timezones) AND
    c.disabled IS NULL AND
    cds.calendar_id IS NULL;


-- name: get_statistics_parsing_config^
SELECT
    user_id,
    skip_all_day_events,
    skip_rejected_meetings
FROM pt.statistics_parsing_config
WHERE 
    user_id = :user_id;