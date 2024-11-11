-- name: save_statistics
INSERT INTO pt.statistics (calendar_id, date, minutes)
VALUES (
    :calendar_id,
    :date,
    :minutes
);
