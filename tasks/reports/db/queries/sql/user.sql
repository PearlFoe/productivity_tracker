-- name: get_user_telegram_id$
SELECT
    telegram_id
FROM pt.user
WHERE
    id = :user_id;

-- name: get_users_to_send_report
SELECT
    s.id,
    s.user_id
FROM pt.schedule s
WHERE 
    EXTRACT(HOUR FROM s.time AT TIME ZONE 'Etc/UTC') = EXTRACT(HOUR FROM CURRENT_TIME);