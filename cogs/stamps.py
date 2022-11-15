import json
import logging
import aiohttp
from pathlib import Path
import discord
from discord import Embed, Webhook
from discord.ext import commands

IMAGE_SUFFIXES = {'.gif', '.jpeg', '.jpg', '.png', '.mp4', '.webm'}
IMAGE_AND_JSON_SUFFIXES = set(IMAGE_SUFFIXES)
IMAGE_AND_JSON_SUFFIXES.add('.json')


def snake_to_camel(name):
    """Converts snake_case to CamelCase"""
    return "".join(word.capitalize() for word in name.split("_"))


def snake_to_title(name):
    """Converts snake_case to Title Case"""
    return " ".join(word.capitalize() for word in name.split("_"))


class Stamps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category_stamp_names = dict()
        self.category_names = []
        self._walk_root()

    def _walk_root(self):
        """Registers stamp commands for each image in each category
        category can be configured with .json file of the same name
        prefix will append the string to all the stamps inside
        """
        root = Path('./stamps')
        root.mkdir(exist_ok=True)

        for category_path in root.iterdir():
            if category_path.is_dir():
                category_config = {
                    'hidden': True,
                    'name': snake_to_camel(category_path.stem),
                    'prefix': '',
                    'message': f'{snake_to_title(category_path.stem)} stamps\n```{{}}```',
                    'file': None
                }

                # Try to find path to thumbnail
                for ext in IMAGE_SUFFIXES:
                    thumb_path = root / f'{category_path.stem}{ext}'
                    if thumb_path.exists():
                        category_config['file'] = thumb_path
                        break

                try:
                    with category_path.with_suffix('.json').open() as fp:
                        category_config.update(json.load(fp))
                except IOError as e:
                    pass  # Ignore if not found

                category_name = category_config['name']
                self.category_names.append(category_name)

                # config_str = f' {category_config}' if category_config else ''
                # print(f'{category_path}{config_str}')

                stamp_names = self._walk_category(category_path, prefix=category_config['prefix'])

                self.category_stamp_names[category_name] = stamp_names

                category_config['stamp_names'] = stamp_names

                cmd = self._category_command(category_config)
                self.bot.add_command(cmd)

    def _category_command(self, config):
        """Generate a dynamic category command object"""
        hidden = config['hidden']
        name = config['name']
        file = config['file']
        message = config['message']
        stamp_names = config['stamp_names']

        formatted_message = message.format(" ".join(stamp_names)).strip()

        @commands.command(
            hidden=hidden,  # Don't show category commands in the usual help
            name=name,
            help=f'Info about {name} stamp category'
        )
        async def cmd(cog: Stamps, ctx: commands.Context):
            final_file = None if file is None else discord.File(file)
            await ctx.send(formatted_message, file=final_file)

        cmd.cog = self
        # Workaround for discord.py heuristic for calculating params to skip by if a function is in a class.
        cmd.params.pop("ctx")

        return cmd

    def _walk_category(self, category_path: Path, prefix=""):
        """Registers commands for all the stamps inside
        Stamp can be configured with .json file
        returns the name of all the commands
        """
        stamp_names = []

        stamp_dict = dict()

        # Collect image and config for each image
        for stamp_path in category_path.iterdir():
            if stamp_path.is_file() and stamp_path.suffix in IMAGE_AND_JSON_SUFFIXES:
                key = stamp_path.stem
                if key not in stamp_dict:
                    # Stamp Config Defaults
                    stamp_dict[key] = {
                        'hidden': True,
                        'name': f'{prefix}{snake_to_camel(stamp_path.stem)}',
                        'aliases': [],
                        'message': '',
                        'file': None,
                    }
                stamp_config = stamp_dict[key]

                if stamp_path.suffix in IMAGE_SUFFIXES:
                    stamp_config['file'] = stamp_path
                else:
                    try:
                        with stamp_path.with_suffix('.json').open() as fp:
                            stamp_config.update(json.load(fp))
                    except IOError as e:
                        pass  # Ignore if not found

        # Create and add a dynamic command for each config object
        for stamp_config in stamp_dict.values():
            stamp_names.append(stamp_config['name'])

            # print(f'{stamp_path} {stamp_config}')
            cmd = self._stamp_command(stamp_config)
            self.bot.add_command(cmd)

        return stamp_names

    def _stamp_command(self, config):
        """Generate a dynamic stamp command object"""
        name = config['name']
        file = config['file']
        aliases = config['aliases']
        message = config['message']
        hidden = config['hidden']

        @commands.command(
            hidden=hidden,
            name=name,
            aliases=aliases,
            help=f'Send {name} stamp'
        )
        async def cmd(cog: commands.Cog, ctx: commands.Context, *args, **kwargs):
            log = logging.getLogger("cogs.stamps")
            final_file = None if file is None else discord.File(file)
            channel_name = ctx.channel.name
            wh_info_found = None
            for wh_info in await ctx.guild.webhooks():
                if wh_info.channel.name == channel_name:
                    wh_info_found = wh_info
                    break
            if wh_info_found is None:
                await ctx.send(
                    f'Missing webhook for #{channel_name}',
                    delete_after=8)
                return
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(wh_info_found.url, session=session)
                if webhook is None:
                    log.error(f'Unable find a webhook in #{channel_name}!')
                    await ctx.send(f'Unable find a webhook in #{channel_name}!', delete_after=8)
                    return
                await ctx.message.delete()
                await webhook.send(avatar_url=f'{ctx.author.avatar_url}', username=ctx.author.display_name, content=message, file=final_file)

        cmd.cog = self
        # Workaround for discord.py heuristic for calculating params to skip by if a function is in a class.
        cmd.params.pop("ctx")

        return cmd

    @commands.command()
    async def stamps(self, ctx):
        """Prints out a list of stamp categories"""
        categories = " ".join(self.category_names)
        await ctx.send(f'Here\'s a list of our stamp packs!\nType `{self.bot.command_prefix}[pack-name]` to see a list of the stamps inside of that pack.```{categories}``` Also, you can add stamps in the `!shop`!'.strip())


async def setup(bot):
    await bot.add_cog(Stamps(bot))
