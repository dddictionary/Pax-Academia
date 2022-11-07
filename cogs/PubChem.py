import pubchempy as pcp
from discord import option
from discord.ext import commands

from util.EmbedBuilder import EmbedBuilder
from util.Logging import log


async def get_data(name: str) -> dict:
    compound = pcp.get_compounds(name, "name")
    return {
        "exact_mass": compound[0].exact_mass,
        "iupac_name": compound[0].iupac_name,
        "charge": compound[0].charge,
        "cid": compound[0].cid,
        "complexity": compound[0].complexity,
        "molecular_formula": compound[0].molecular_formula,
        "molecular_weight": compound[0].molecular_weight,
        "tpsa": compound[0].tpsa,
        "xlogp": compound[0].xlogp,
    }


class PubChem(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def to_subscript(self, number: int) -> str:
        subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return str(number).translate(subscript)

    @commands.slash_command(
        name="chemsearch", description="Searches the database for a compound."
    )
    @option(
        name="name",
        description="The name of the compound to be searched.",
        required=True,
    )
    async def pubchem(self, ctx: commands.Context, name: str) -> None:
        try:
            data = await get_data(name)
            embed = EmbedBuilder(
                title=f"Properties of __{name.title()}__",
                url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{data['cid']}",
                description=f"**IUPAC Name:**\n{data['iupac_name']}",
                fields=[
                    [
                        "Molecular Formula",
                        self.to_subscript(data["molecular_formula"]),
                        True,
                    ],
                    ["Exact Mass", round(float(data["exact_mass"]), 2), True],
                    ["Charge", data["charge"], True],
                    ["Molecular Weight", data["molecular_weight"], True],
                    ["XLogP", data["xlogp"], True],
                    ["TPSA", data["tpsa"], True],
                    ["Complexity", data["complexity"], True],
                ],
                image=f"https://pubchem.ncbi.nlm.nih.gov/image/imagefly.cgi?cid={data['cid']}&width=400&height=400",
            ).build()

            await ctx.respond(embed=embed)

            log(f"Chemsearch command used by {ctx.author} in {ctx.guild}.")

        except IndexError:
            embed = EmbedBuilder(
                title="Error",
                description=f"Compound **{name.title()}** not found. Did you spell it correctly?",
            ).build()

            await ctx.respond(embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(PubChem(bot))
