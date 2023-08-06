import discord
from cogs.Tips import send_tip
from contextlib import suppress
from discord.ext import commands
from os import getenv
from util.Logging import Log


class DetectCode(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.cs_category_id = int(getenv("UNFORMATTED_CODE_DETECTION_CATEGORY_ID", -1))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if (
            message.author.bot
            or message.channel.category.id != self.cs_category_id
            or "```" in message.content
        ):
            return
        # Set threshhold for the probability of text being code
        # You can adjust this value based on your preferences
        minimum_code_probability = 0.5

        lines = message.content.splitlines()

        # Most people don't paste one line of code, so this avoids false positives
        if len(lines) == 1:
            return

        non_blank_lines = [line for line in lines if line.strip()]
        code_like_lines = [
            line
            for line in non_blank_lines
            if any(
                [
                    line.startswith(("  ")),
                    line.endswith((";", "{", "}", "]", "[", ")", "(", ":", ",")),
                ]
            )
        ]

        # Calculate the percentage of code-like lines
        percentage_code_like = (
            len(code_like_lines) / len(non_blank_lines) if non_blank_lines else 0
        )

        if percentage_code_like >= minimum_code_probability:
            await send_tip(message.channel, "Format Your Code", message.author, "bot")
            with suppress(AttributeError):
                Log(
                    f" $ sent potential code in {message.channel.name}, bot responded with tip",
                    message.author,
                )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(DetectCode(bot))
