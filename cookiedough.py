import asyncio
import logging
import pathlib
import sys

import discord
from discord.ext import commands

# The testing cog will be skipped if this is not set to True.
TEST_MODE = False


async def main():
    discord.utils.setup_logging(level=logging.INFO)
    log = logging.getLogger("main")

    description = '''A cookie loving Discord bot'''
    intents = discord.Intents.all()
    bot = commands.Bot(
        description=description,
        intents=intents,
        command_prefix='.',
        case_insensitive=True,
    )

    async def load_extension_safe(name: str):
        try:
            await bot.load_extension(name)
        except commands.ExtensionError as e:
            log.exception(f'Exception when loading extension {name}', exc_info=e)

    await asyncio.gather(*[load_extension_safe(name) for name in get_cog_extension_names()])

    await bot.start(sys.argv[1])


def get_cog_extension_names():
    cd_path = pathlib.Path(".")
    cogs_path = cd_path / "cogs"

    cog_extension_names = []

    for cog_path in cogs_path.glob("**/*.py"):
        if not cog_path.is_file():
            continue

        if not TEST_MODE and cog_path.stem == "testing":
            continue

        assert cog_path.is_relative_to(cd_path)
        cog_extension_name = cog_path.with_suffix('').relative_to(cd_path).as_posix().replace("/", ".")

        cog_extension_names.append(cog_extension_name)

    return cog_extension_names


if __name__ == "__main__":
    asyncio.run(main())
