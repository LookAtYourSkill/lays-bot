import disnake
from disnake.ext import commands


class Bet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Creates a bet')
    async def bet(self, inter: disnake.ApplicationCommandInteraction, target: disnake.Member, einsatz="Ehre", *, wette):
        if target.bot:
            embed = disnake.Embed(
                description="Du kannst keine Wette gegen einen Bot machen",
                color=disnake.Color.red()
            )
            await inter.response.send_message(
                embed=embed
            )
        elif inter.author == target:
            embed = disnake.Embed(
                description="Du kannst keine Wette gegen dich selbst machen",
                color=disnake.Color.red()
            )
            await inter.response.send_message(
                embed=embed
            )
        else:
            bet_embed = disnake.Embed(
                description=f"{inter.author.mention} hat eine Wette gegen {target.mention} gestartet! In dieser Wette geht es um `{wette}` und der Preis ist `{einsatz}`\n"
                            f"\n"
                            f"{target.mention} du musst nurnoch mit `accept` im Chat innerhalb von `60 Sekunden` antworten!",
                color=disnake.Color.green()
            )

            await inter.response.send_message(
                content=target.mention,
                embed=bet_embed
            )

            def check(m):
                return m.author == target
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)
                if msg.content == "accept".lower():
                    accept_embed = disnake.Embed(
                        description=f'{target.mention} hat die Wette **angenommen**! Die Wette zwischen {inter.author.mention} und {target.mention} **gilt ab nun** und es geht um `{einsatz}`.',
                        color=disnake.Color.green()
                    )
                    await inter.send(
                        embed=accept_embed
                    )
            except disnake.InteractionTimedOut:
                decline_embed = disnake.Embed(
                    description=f'{target.mention} entweder hast du zu **lange gebraucht**, oder du wolltest es **nicht annehmen**. Somit gilt diese Wette **nicht**!'
                )
                await inter.send(
                    embed=decline_embed
                )


def setup(bot):
    bot.add_cog(Bet(bot))
