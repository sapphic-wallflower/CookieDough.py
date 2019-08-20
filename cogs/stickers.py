import json
from pathlib import Path

import discord
from discord.ext import commands

IMAGE_SUFFIXES = {'.gif', '.jpeg', '.jpg', '.png'}


class Stickers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category_sticker_names = dict()
        self.category_names = []
        self._walk_root()

    def _walk_root(self):
        """Registers sticker commands for each image in each category
        category can be configured with .json file of the same name
        prefix will append the string to all the stickers inside
        """
        root = Path('./stickers')
        root.mkdir(exist_ok=True)

        for category_path in root.iterdir():
            if category_path.is_dir():
                category_config = {
                    'name': f'{category_path.stem}',
                    'prefix': '',
                    'message': f'{category_path.stem} stickers\n`{{}}`'
                }
                try:
                    with category_path.with_suffix('.json').open() as fp:
                        category_config.update(json.load(fp))
                except IOError as e:
                    pass  # Ignore if not found

                category_name = category_config['name']
                self.category_names.append(category_name)

                # config_str = f' {category_config}' if category_config else ''
                # print(f'{category_path}{config_str}')

                sticker_names = self._walk_category(category_path, prefix=category_config['prefix'])

                self.category_sticker_names[category_name] = sticker_names

                cmd = self._category_command(category_name, category_config['message'], sticker_names)
                self.bot.add_command(cmd)

    def _category_command(self, name, message, sticker_names):
        """Generate a dynamic category command object"""

        formatted_message = message.format(" ".join(sticker_names)).strip()

        async def callback(cog, ctx):
            await ctx.send(formatted_message)
            pass

        cmd = commands.Command(
            callback,
            hidden=True,  # Don't show sticker commands in the usual help
            name=name,
            help=f'Info about {name} sticker category'
        )

        cmd.cog = self

        return cmd

    def _walk_category(self, category_path: Path, prefix=""):
        """Registers commands for all the stickers inside
        sticker can be configured with .json file
        returns the name of all the commands
        """
        sticker_names = []

        for sticker_path in category_path.iterdir():
            if sticker_path.is_file() and sticker_path.suffix in IMAGE_SUFFIXES:
                sticker_config = {
                    'name': f'{prefix}{sticker_path.stem}',
                    'message': '',
                    'hidden': True
                }

                try:
                    with sticker_path.with_suffix('.json').open() as fp:
                        sticker_config.update(json.load(fp))
                except IOError as e:
                    pass  # Ignore if not found

                sticker_names.append(sticker_config['name'])

                # print(f'{sticker_path} {sticker_config}')
                cmd = self._sticker_command(sticker_config['name'], sticker_path, sticker_config['message'], sticker_config['hidden'])
                self.bot.add_command(cmd)

        return sticker_names

    def _sticker_command(self, name, file, message=None, hidden=True):
        """Generate a dynamic sticker command object"""

        async def callback(cog, ctx):
            await ctx.send(message, file=discord.File(file))
            pass

        cmd = commands.Command(
            callback,
            name=name,
            help=f'Send {name} sticker',
            hidden=hidden
        )

        cmd.cog = self

        return cmd

    @commands.command()
    async def stickers(self, ctx):
        """Prints out a list of sticker categories"""
        await ctx.send(f'Sticker categories (type .<category> to see the stickers inside)\n`{" ".join(self.category_names)}`'.strip())


def setup(bot):
    bot.add_cog(Stickers(bot))
