-- name: get_user_id^
SELECT id
FROM pt.user AS u
WHERE u.telegram_id = :tg_id;

-- name: create_user!
INSERT INTO pt.user (telegram_id)
VALUES (:tg_id);