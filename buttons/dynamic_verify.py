import disnake

from config.app_config import config
from config.messages import Messages
from features import dynamic_verify


class DynamicVerifyRequestView(disnake.ui.View):
    def __init__(self, rule_id: str, user_id: int):
        self.rule_id = rule_id
        self.user_id = user_id
        super().__init__(timeout=None)

    @disnake.ui.button(label="Schválit", style=disnake.ButtonStyle.success, custom_id="dynamic_verify:accept")
    async def accept_access(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        service = dynamic_verify.DynamicVerifyManager(inter.bot)
        await service.apply_rule(self.rule_id, self.user_id, inter)
        self.clear_items()
        await self.message.edit(view=self)

    @disnake.ui.button(
        label="Zamítnout", style=disnake.ButtonStyle.danger, custom_id="dynamic_verify:decline"
    )
    async def decline_access(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.message.delete()

        guild = inter.guild if inter.guild is not None else inter.bot.get_guild(config.guild_id)
        member = await guild.get_or_fetch_member(self.user_id)
        if member is not None:
            try:
                await member.send(Messages.dynamic_verify_declined)
            except disnake.HTTPException:
                pass
