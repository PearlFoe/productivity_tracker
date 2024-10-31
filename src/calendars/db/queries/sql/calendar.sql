-- name: add_calendar^
INSERT INTO pt.calendar (user_id, name, description, timezone)
VALUES (
    (
        SELECT u.id 
        FROM pt.user as u
        WHERE u.tg_id = :tg_id
    ),
    :name,
    :description,
    :timezone
)
RETURNING pt.calendar.id;

-- name: update_calendar_category!
UPDATE pt.calendar (category)
VALUES (
    (
        SELECT с.id 
        FROM pt.calendar_category as с
        WHERE c.name = :category
    )
)
WHERE pt.calendar.id = :calendar_id;