-- :macro update_moderators(batch_size)
INSERT INTO moderators (id)
VALUES (
	-- :for n in range(1, batch_size + 1)
	(${{ n }}){% if not loop.last %}, {% endif %}
	-- :endfor
)
ON CONFLICT DO NOTHING
-- :endmacro

-- :macro add_moderator()
-- params: user_id
{{ update_moderators(1) }}
-- :endmacro

-- :macro delete_moderator()
-- params: user_id
DELETE FROM moderators
WHERE id = $1
-- :endmacro
