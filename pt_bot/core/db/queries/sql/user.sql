-- name: get_user^
SELECT
    id,
    telegram_id
FROM pt.user
WHERE 
    telegram_id = :telegram_id;
