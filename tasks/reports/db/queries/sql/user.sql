-- name: get_user_telegram_id$
SELECT
    telegram_id
FROM pt.user
WHERE
    id = :user_id;