--  © 2020 lambda#0987
--
-- Murder Mason is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as
-- published by the Free Software Foundation, either version 3 of the
-- License, or (at your option) any later version.
--
-- Murder Mason is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU Affero General Public License for more details.
--
-- You should have received a copy of the GNU Affero General Public License
-- along with Murder Mason. If not, see <https://www.gnu.org/licenses/>.

-- This file must be run in the same database as Emote Collector.

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
