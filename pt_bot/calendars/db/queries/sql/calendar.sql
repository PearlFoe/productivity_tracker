-- name: add_calendar<!
INSERT INTO pt.calendar (user_id, google_id, name, description, timezone)
VALUES (
    (
        SELECT u.id 
        FROM pt.user u
        WHERE u.telegram_id = :tg_id
    ),
    :google_id,
    :name,
    :description,
    :timezone
)
RETURNING id;

-- name: update_calendar_category!
UPDATE pt.calendar c
SET 
    category=(
        SELECT cc.id 
        FROM pt.calendar_category cc
        WHERE cc.name = :category
    )
WHERE c.id = :calendar_id;

-- name: add_schedule!
INSERT INTO pt.schedule
(user_id, name, time)
VALUES (:user_id, :name, :time);