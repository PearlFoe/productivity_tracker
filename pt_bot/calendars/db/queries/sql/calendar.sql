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

-- name: user_has_schedule$
SELECT
    EXISTS(
        SELECT id
        FROM pt.schedule
        WHERE 
            user_id = :user_id
    );

-- name: add_schedule!
INSERT INTO pt.schedule
(user_id, name, time)
VALUES (:user_id, :name, :time);

-- name: disable_calendar!
UPDATE pt.calendar
SET disabled=now()
WHERE 
    user_id = :user_id AND
    name = :calendar_name;

-- name: get_calendar_names
SELECT
    name
FROM pt.calendar
WHERE
    user_id = :user_id AND
    disabled IS NULL;