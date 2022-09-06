import disnake
from disnake.ext import commands
from datetime import datetime

from utils.twitter import get_user


class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="twitter",
        description="Group command for Twitter"
    )
    async def twitter(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @twitter.sub_command(
        name="info",
        description="Get information about a Twitter user"
    )
    async def twitter_info(self, interaction: disnake.ApplicationCommandInteraction, user: str):
        await interaction.response.defer(ephemeral=True)

        loading_embed = disnake.Embed(
            title="Loading...",
            description="Please wait while I gather information about this user...",
            color=disnake.Color.blue()
        )
        await interaction.edit_original_message(
            embed=loading_embed
        )

        try:
            twitterUser = get_user(user)

            accountTime = twitterUser["created_at"]
            changedTime = accountTime[:19] + "Z"
            # format time to datetime timestamp
            finalTime = datetime.strptime(changedTime, '%Y-%m-%dT%H:%M:%SZ').timestamp()

            embed = disnake.Embed(
                color=disnake.Color.blue()
            )
            embed.set_author(
                name="Twitter User Info",
                icon_url="https://cdn.discordapp.com/attachments/948251167501197342/1004814709851168959/unknown.png",
                url="https://twitter.com"
            )
            embed.set_thumbnail(url=twitterUser["profile_image_url"])
            embed.add_field(
                name="__Information__",
                value=f"**Name:** `{twitterUser['name']}`\n"
                    f"**Username:** `{twitterUser['username']}`\n"
                    f"**ID:** `{twitterUser['id']}`\n"
                    f"**Description:** `{twitterUser['description'] if twitterUser['description'] else 'No description'}`\n"
                    f"**Follower:** `{twitterUser['public_metrics']['followers_count']}`\n"
                    f"**Following:** `{twitterUser['public_metrics']['following_count']}`\n"
                    f"**Tweets:** `{twitterUser['public_metrics']['tweet_count']}`\n"
                    f"**Website** [Click here]({twitterUser['url'] if twitterUser['url'] else 'https://twitter.com'})\n"
                    f"**Verified:** `{'Yes' if twitterUser['verified'] else 'No'}`\n"
                    f"**Created At:** <t:{int(finalTime)}:f>",
                inline=False
            )

            await interaction.edit_original_message(
                embed=embed
            )

        except Exception as e:
            embed = disnake.Embed(
                title="Error :x:",
                description=f"User [`{user}`] not found!\n"
                            f"Please **try it again later** or **check the spelling** of the username!",
                color=disnake.Color.red()
            )

            await interaction.edit_original_message(
                embed=embed
            )


def setup(bot):
    bot.add_cog(Twitter(bot))
