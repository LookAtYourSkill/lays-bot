import disnake
import praw
import random

from disnake.ext import commands


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="meme")
    async def meme(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @meme.sub_command(name="reddit")
    async def meme_reddit(self, interaction: disnake.ApplicationCommandInteraction):
        loading_embed = disnake.Embed(
            description="Getting memes from Reddit...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        reddit = praw.Reddit(
            client_id="e3WCWP0by7A_vptAGIULKA",
            client_secret="lqutAcUFkFkdsSHxICYkqKRjyubYPw",
            user_agent="pythonpraw",
            check_for_async=False
        )

        memes = ["funnymeme", "memes", "meme", "dankmemes", "lolmemes"]

        try:
            subreddit = reddit.subreddit(random.choice(memes))
            all_subs = []
            top = subreddit.top(limit=100)

            for submission in top:
                all_subs.append(submission)

            random_sub = random.choice(all_subs)

            embed = disnake.Embed(
                title=random_sub.title,
                color=disnake.Colour.random()
            )
            embed.set_image(
                url=random_sub.url
            )
            embed.set_footer(
                text=f"Requested by {interaction.author.display_name}",
                icon_url=interaction.author.avatar_url
            )

            await interaction.edit_original_message(
                embed=embed
            )
        except Exception as e:
            await interaction.followup(
                e
            )
            em = disnake.Embed(
                title="No Meme Found"
            )
            await interaction.edit_original_message(
                embed=em
            )


def setup(bot):
    bot.add_cog(Meme(bot))
