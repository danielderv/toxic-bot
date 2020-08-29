from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command

from ..db import db


class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("welcome")

	@Cog.listener()
	async def on_member_join(self, member):
		db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
		await self.bot.get_channel(743536831488065626).send(f"Welcome to **{member.guild.name}** {member.mention}! Head over to <#626608699942764548> to say hi!")

		try:
			await member.send(f"Welcome to **{member.guild.name}**! Enjoy your stay!")

		except Forbidden:
			pass

		await member.add_roles(member.guild.get_role(743532339186892861), member.guild.get_role(743532339186892861))

	@Cog.listener()
	async def on_member_remove(self, member):
		db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
		await self.bot.get_channel(743537138796331069).send(f"{member.display_name} has left {member.guild.name}.")


def setup(bot):
	bot.add_cog(Welcome(bot))