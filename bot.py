import discord
from ext.formatter import EmbedHelp
from discord.ext import commands
from contextlib import redirect_stdout
import datetime
import json
import inspect
import os
import glob
import io
import textwrap
import traceback
import asyncio
from cogs.utils.dataIO import dataIO
data = {}
defaultdata = {
"BOT": {
	"TOKEN" : 'insert token here',
	"PREFIX" : 's.'
	},
"FIRST" : True
}
token = ''
prefix = ''
def run_wizard():
	print('------------------------------------------')
	print('WELCOME TO THE VERIX-SELFBOT SETUP WIZARD!')
	print('------------------------------------------')
	token = input('Enter your token:\n> ')
	print('------------------------------------------')
	prefix = input('Enter a prefix for your selfbot:\n> ')
	if prefix == '':
		prefix = 's.'
	data = {
		"BOT": {
			"TOKEN" : token,
			"PREFIX" : prefix
			},
		"FIRST" : False
		}
	with open('data/config.json','w') as f:
		f.write(json.dumps(data, indent=4))
	print('------------------------------------------')
	print('Successfully saved your data!')
	print('------------------------------------------')
heroku = False
if 'DYNO_RAM' in os.environ:
	heroku = True
	TOKEN = os.environ['TOKEN']
else:
	heroku = False
	if not os.path.exists('data'):
		os.makedirs('data')

	try:
		open('data/config.json')
	except:
		with open('data/config.json','w+') as f:
			f.write(json.dumps(defaultdata, indent=4))

	with open('data/config.json') as f:
		if json.load(f)['FIRST']:
			run_wizard()

	with open('data/config.json') as f:  
		TOKEN = json.load(f)["BOT"]['TOKEN']

async def get_pre(bot, message):

	if 'PREFIX' in os.environ:
		return os.environ['PREFIX']
		
	with open('data/config.json') as f:
		config = json.load(f)
	try:
		return config["BOT"]['PREFIX']
	except:
		return 's.'

bot = commands.Bot(command_prefix=get_pre, self_bot=True, formatter=EmbedHelp())
bot.remove_command('help')
_extensions = [

	# 'cogs.clashroyale',
	'cogs.misc',
	'cogs.utility',
	'cogs.utils2',
	'cogs.info',
	'cogs.mod',
	'cogs.stuff',
	'cogs.react',
	'cogs.crtags',
	'cogs.trophy',
	'cogs.info2'
	]

NOBPATH = os.path.join('data', 'nob')
NOB_JSON = os.path.join(NOBPATH,  'settings.json')

def check_foldernob():
	if not os.path.exists(NOBPATH):
		os.makedirs(NOBPATH)

def check_filenob():
	defaults = {'hasname':False, 'nob':False, 'breplace' : False}
	print(NOB_JSON)
	if not dataIO.is_valid_json(NOB_JSON):
		dataIO.save_json(NOB_JSON, defaults)
		
check_foldernob()
check_filenob()

@asyncio.coroutine
def on_message2(message):
	# print(message.author)
#     if message.author == bot.user:
#         return
	# print('lol i enterd a msg')
	if bot.user != message.author:
		return
	print(message)
	dukeserver = bot.get_server('249979148246843393') #if you are in racf dont
	a = message.content
	nobdict = {}
	nobdict = dataIO.load_json(NOB_JSON) 
	if '`togglenob`' in a:
		nobdict['nob'] = not nobdict['nob']
		dataIO.save_json(NOB_JSON, nobdict)
	print(nobdict)
	if heroku==True:
		prefix = os.environ['PREFIX']
		if message.content.startswith(prefix):
			yield from bot.process_commands(message)
			return
	if not dataIO.load_json(NOB_JSON)['nob'] and not (a == '' or a == None or '`nob`' in a):
		b = ''
		hasname = nobdict['hasname']
		if '`togglename`' in a:
			nobdict['hasname'] = not hasname
			dataIO.save_json(NOB_JSON, nobdict)
		for i, letter in enumerate(a):
			if(i==0 and letter.isalpha()):
				b += '🅱️'
			elif((not a[i-1].isalpha()) and letter.isalpha()):
				b += '🅱️'
			else:
				b += letter
		yield from bot.delete_message(message)
		if hasname:
			yield from bot.send_message(channel,'{}: {}'.format(message.author.display_name, b))
		else:
			yield from bot.send_message(channel,'{}'.format(b))
		
	yield from bot.process_commands(message)
	
# @asyncio.coroutine
# def on_message2(message):
#     # print(message.author)
#     if message.author != bot.user:
#         return
#     # print('lol i enterd a msg')
#     racfserver = bot.get_server('218534373169954816') #if you are in racf dont
#     if message.server == racfserver:				# use it on that server
#         return
#     yield from bot.process_commands(message)

# @asyncio.coroutine
# def myon_member_join(member):


#     randomserv = bot.get_server('354544842845716480')
#     randomserv = bot.get_server('351873361023991821')
#     testystuff = randomserv.get_channel('355724086149906434')
#     testystuff = randomserv.get_channel('351873361023991821')
	
#     try:
#         servinvites = yield from bot.invites_from(member.server)
#     except:
#         servinvites = []
#     # x = randomserv
#     # print('***********************')
#     # print(x)
#     # print('*********type**********')
#     # print(type(x))
#     # print('**********dir**********')
#     # print(dir(x))
#     # print('***********************')
#     x = randomserv.channels
#     print('***********************')
#     print(x)
#     print('*********type**********')
#     print(type(x))
#     print('**********dir**********')
#     print(dir(x))
#     print('***********************')

#     server = randomserv
#     # channels = list(server.channels)
#     # channelsend = channels[0]
#     channels = list(server.channels)
#     print(type(channels))
#     # for chan in channels:
#     #     print(chan)
#     channelsend = None
#     for channel in channels:
#         if channelsend == None or (channelsend.created_at > channel.created_at and channel.type == 'text'):
#             channelsend = channel


#     yield from bot.send_message(channelsend, 'Welcome to {}, {}!'.format(member.server.name, member.name))
#     # print('Welcome to {}, {}!'.format(member.server.name, member.name+'#'+member.discriminator))
#     invite = None
#     # inviter = invite.inviter

@bot.event
async def on_ready():
	# bot.on_member_join = myon_member_join
	if bot.user.id == '222925389641547776':
		bot.on_message = on_message2
	bot.uptime = datetime.datetime.now()
	prefix = await get_pre(bot, ' ')
	x =   [
		'------------------------------------------',
		'Self-Bot Ready',
		'Author: verix#7220',
		'Some Cogs/Cmds By: Dino#0631',
		'------------------------------------------',
		'Username: {}'.format(bot.user),
		'User ID: {}'.format(bot.user.id),
		'Prefix: {}'.format(prefix),
		'------------------------------------------'
	]
	print('\n'.join(x))
	if heroku:
		print('Hosting on heroku.')





@bot.command(pass_context=True)
async def ping(ctx):
	"""Pong! Check your response time."""
	msgtime = ctx.message.timestamp.now()
	await (await bot.ws.ping())
	now = datetime.datetime.now()
	ping = now - msgtime
	pong = discord.Embed(title='Pong! Response Time:', 
						 description=str(ping.microseconds / 1000.0) + ' ms',
						 color=0x00ffff)

	await bot.say(embed=pong)

@bot.command(pass_context=True)
async def shutdown(ctx):
	"""Restarts the selfbot."""
	channel = ctx.message.channel
	await bot.say("Shutting down...")
	await bot.logout()

	
# @bot.command(name='presence')
# async def _set(Type,*,message=None):
#     """Change your discord game/stream!"""
#     if Type.lower() == 'stream':
#         await bot.change_presence(game=discord.Game(name=message,type=1,url='https://www.twitch.tv/{}'.format(message)),status='online')
#         await bot.say('Set presence to. `Streaming {}`'.format(message))
#     elif Type.lower() == 'game':
#         await bot.change_presence(game=discord.Game(name=message))
#         await bot.say('Set presence to `Playing {}`'.format(message))
#     elif Type.lower() == 'clear':
#         await bot.change_presence(game=None)
#         await bot.say('Cleared Presence')
#     else:
#         await bot.say('Usage: `.presence [game/stream/clear] [message]`')

# async def send_cmd_help(ctx):
#     if ctx.invoked_subcommand:
#         pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
#         for page in pages:
#             print(page)
#             await bot.send_message(ctx.message.channel, embed=page)
#         print('Sent command help')
#     else:
#         pages = bot.formatter.format_help_for(ctx, ctx.command)
#         for page in pages:
#             print(page)
#             await bot.send_message(ctx.message.channel, embed=page)
#         print('Sent command help')

# # @bot.event
# # async def on_message(message):
# #     try:
# #         print("{} from {}\n{}".format(message.author,message.server, message.content))
# #     except:
# #         pass



# @bot.event
# async def on_command_error(error, ctx):
#    print(error)
#    channel = ctx.message.channel
#    if isinstance(error, commands.MissingRequiredArgument):
#        await send_cmd_help(ctx)
#        print('Sent command help')
#    elif isinstance(error, commands.BadArgument):
#        await send_cmd_help(ctx)
#        print('Sent command help')
#    elif isinstance(error, commands.DisabledCommand):
#        await bot.send_message(channel, "That command is disabled.")
#        print('Command disabled.')
#    elif isinstance(error, commands.CommandInvokeError):
#        # A bit hacky, couldn't find a better way
#        no_dms = "Cannot send messages to this user"
#        is_help_cmd = ctx.command.qualified_name == "help"
#        is_forbidden = isinstance(error.original, discord.Forbidden)
#        if is_help_cmd and is_forbidden and error.original.text == no_dms:
#            msg = ("I couldn't send the help message to you in DM. Either"
#                   " you blocked me or you disabled DMs in this server.")
#            await bot.send_message(channel, msg)
#            return



# @bot.command(pass_context=True, aliases=['cogs'])
# async def coglist(ctx):
#     '''See unloaded and loaded cogs!'''
#     def pagify(text, delims=["\n"], *, escape=True, shorten_by=8,
#                page_length=2000):
#         """DOES NOT RESPECT MARKDOWN BOXES OR INLINE CODE"""
#         in_text = text
#         if escape:
#             num_mentions = text.count("@here") + text.count("@everyone")
#             shorten_by += num_mentions
#         page_length -= shorten_by
#         while len(in_text) > page_length:
#             closest_delim = max([in_text.rfind(d, 0, page_length)
#                                  for d in delims])
#             closest_delim = closest_delim if closest_delim != -1 else page_length
#             if escape:
#                 to_send = escape_mass_mentions(in_text[:closest_delim])
#             else:
#                 to_send = in_text[:closest_delim]
#             yield to_send
#             in_text = in_text[closest_delim:]
#         yield in_text

#     def box(text, lang=""):
#         ret = "```{}\n{}\n```".format(lang, text)
#         return ret
#     loaded = [c.__module__.split(".")[1] for c in bot.cogs.values()]
#     # What's in the folder but not loaded is unloaded
#     def _list_cogs():
#           cogs = [os.path.basename(f) for f in glob.glob("cogs/*.py")]
#           return ["cogs." + os.path.splitext(f)[0] for f in cogs]
#     unloaded = [c.split(".")[1] for c in _list_cogs()
#                 if c.split(".")[1] not in loaded]

#     if not unloaded:
#         unloaded = ["None"]

#     em1 = discord.Embed(color=discord.Color.green(), title="+ Loaded", description=", ".join(sorted(loaded)))
#     em2 = discord.Embed(color=discord.Color.red(), title="- Unloaded", description=", ".join(sorted(unloaded)))
#     await bot.say(embed=em1)
#     await bot.say(embed=em2)


# def cleanup_code( content):
#     """Automatically removes code blocks from the code."""
#     # remove ```py\n```
#     if content.startswith('```') and content.endswith('```'):
#         return '\n'.join(content.split('\n')[1:-1])

#     # remove `foo`
#     return content.strip('` \n')

# def get_syntax_error(e):
#     if e.text is None:
#         return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
#     return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

# async def to_code_block(ctx, body):
#     if body.startswith('```') and body.endswith('```'):
#         content = '\n'.join(body.split('\n')[1:-1])
#     else:
#         content = body.strip('`')
#     await bot.edit_message(ctx.message, '```py\n'+content+'```')

# @bot.command(pass_context=True, name='eval')
# async def _eval(ctx, *, body: str):
#     '''Run python scripts on discord!'''
#     await to_code_block(ctx, body)
#     env = {
#         'bot': bot,
#         'ctx': ctx,
#         'channel': ctx.message.channel,
#         'author': ctx.message.author,
#         'server': ctx.message.server,
#         'message': ctx.message,
#     }

#     env.update(globals())

#     body = cleanup_code(content=body)
#     stdout = io.StringIO()

#     to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

#     try:
#         exec(to_compile, env)
#     except SyntaxError as e:
#         return await bot.say(get_syntax_error(e))

#     func = env['func']
#     try:
#         with redirect_stdout(stdout):
#             ret = await func()
#     except Exception as e:
#         value = stdout.getvalue()
#         x = await bot.say('```py\n{}{}\n```'.format(value, traceback.format_exc()))
#         try:
#             await bot.add_reaction(x, '\U0001f534')
#         except:
#             pass
#     else:
#         value = stdout.getvalue()
		
#         if TOKEN in value:
#             value = value.replace(TOKEN,"[EXPUNGED]")
			
#         if ret is None:
#             if value:
#                 try:
#                     x = await bot.say('```py\n%s\n```' % value)
#                 except:
#                     x = await bot.say('```py\n\'Result was too long.\'```')
#                 try:
#                     await bot.add_reaction(x, '\U0001f535')
#                 except:
#                     pass
#             else:
#                 try:
#                     await bot.add_reaction(ctx.message, '\U0001f535')
#                 except:
#                     pass
#         else:
#             try:
#                 x = await bot.say('```py\n%s%s\n```' % (value, ret))
#             except:
#                 x = await bot.say('```py\n\'Result was too long.\'```')
#             try:
#                 await bot.add_reaction(x, '\U0001f535')
#             except:
#                 pass


# @bot.command(pass_context=True)
# async def say(ctx, *, message: str):
#     '''Say something as the bot.'''
#     if '{}say'.format(ctx.prefix) in message:
#         await bot.say("Don't ya dare spam.")
#     else:
#         await bot.say(message)

# @bot.command(pass_context=True, name='reload')
# async def _reload(ctx, exten=None):
#     '''default reloads all cogs, with arg reloads one cog'''
#     if(exten == None):
#         for extension in _extensions:
#             try:
#                 bot.unload_extension(extension)
#                 bot.load_extension(extension)
#                 await bot.say('Reloaded extension: {}'.format(extension))
#             except Exception as e:
#                 exc = '{}: {}'.format(type(e).__name__, e)
#                 await bot.say('Failed to reload extension {}\n{}'.format(extension, exc))
#     else:
#         exten = 'cogs.' + exten
#         try:
#             bot.unload_extension(exten)
#             bot.load_extension(exten)
#             await bot.say('Reloaded extension: {}'.format(exten))
#         except Exception as e:
#             exc = '{}: {}'.format(type(e).__name__, e)
#             await bot.say('Failed to reload extension {}\n{}'.format(exten, exc))

# @bot.command(pass_context=True)
# async def unload(ctx, exten=None):
#     '''default unloads all cogs, with arg unloads one cog'''
#     if(exten == None):
#         for extension in _extensions:
#             try:
#                 bot.unload_extension(extension)
#                 await bot.say('Unloaded extension: {}'.format(extension))
#             except Exception as e:
#                 exc = '{}: {}'.format(type(e).__name__, e)
#                 await bot.say('Failed to unload extension {}\n{}'.format(extension, exc))
#     else:
#         exten = 'cogs.' + exten
#         try:
#             bot.unload_extension(exten)
#             await bot.say('Unloaded extension: {}'.format(exten))
#         except Exception as e:
#             exc = '{}: {}'.format(type(e).__name__, e)
#             await bot.say('Failed to unload extension {}\n{}'.format(exten, exc))

# @bot.command(pass_context=True)
# async def load(ctx, exten=None):
#     '''default loads all cogs, with arg loads one cog'''
#     if(exten == None):
#         for extension in _extensions:
#             try:
#                 bot.load_extension(extension)
#                 await bot.say('Loaded extension: {}'.format(extension))
#             except Exception as e:
#                 exc = '{}: {}'.format(type(e).__name__, e)
#                 await bot.say('Failed to load extension {}\n{}'.format(extension, exc))
#     else:
#         exten = 'cogs.' + exten
#         try:
#             bot.load_extension(exten)
#             await bot.say('Loaded extension: {}'.format(exten))
#         except Exception as e:
#             exc = '{}: {}'.format(type(e).__name__, e)
#             await bot.say('Failed to load extension {}\n{}'.format(exten, exc))

# if __name__ == "__main__":  
#     for extension in _extensions:
#         try:
#             bot.load_extension(extension)
#             print('Loaded extension: {}'.format(extension))
#         except Exception as e:
#             exc = '{}: {}'.format(type(e).__name__, e)
#             print('Failed to load extension {}\n{}'.format(extension, exc))
			
try:
	print('penis is starting')
	bot.run(TOKEN, bot=False)
except Exception as e:
	print('\n[ERROR]: \n{}\n'.format(e))
	
