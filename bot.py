#!/usr/bin/env python3

# © 2020 lambda#0987
#
# Murder Mason is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Murder Mason is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Murder Mason. If not, see <https://www.gnu.org/licenses/>.

import asyncpg
import jinja2
import discord
import toml

class MurderMason(discord.Client):
	def __init__(self):
		super().__init__(status=discord.Status.idle)
		self.reload_config()
		self.queries = jinja2.Environment(
			loader=jinja2.FileSystemLoader('.'),
			line_statement_prefix='-- :',
		).get_template('queries.sql').module

	async def login(self, token=None, *, bot=True):
		self.pool = await asyncpg.connect(**self.config['database'])
		await super().login(self.config['tokens']['discord'])

	async def close(self):
		await self.pool.close()
		await super().close()

	async def on_ready(self):
		await self.change_presence(status=discord.Status.online)
		await self.update_moderator_list()
		print('Ready')

	def reload_config(self):
		with open('config.toml') as f:
			self.config = toml.load(f)

	async def update_moderator_list(self):
		role = self._moderator_role()
		if not role:
			return

		members = [member.id for member in role.members if not member.bot]
		if members:
			await self.pool.execute(self.queries.update_moderators(len(members)), *members)

	async def on_member_update(self, before, after):
		if before.guild.id != self.config['support_server'].get('id') or after.bot:
			return

		mod_role = self._moderator_role()
		if not mod_role:
			return

		if mod_role in before.roles and mod_role not in after.roles:
			await self.pool.execute(self.queries.delete_moderator(), after.id)
		elif mod_role not in before.roles and mod_role in after.roles:
			await self.pool.execute(self.queries.add_moderator(), after.id)

	def _moderator_role(self):
		guild_id = self.config['support_server'].get('id')
		if not guild_id:
			return

		guild = self.get_guild(guild_id)
		if not guild:
			return

		role_id = self.config['support_server'].get('moderator_role_id')
		if not role_id:
			return

		return guild.get_role(role_id)

if __name__ == '__main__':
	# login() retrieves the token so we don't actually need to pass it
	MurderMason().run(None)
