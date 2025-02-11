import os
import discord
import requests
from discord.ext import commands
from discord import Activity, ActivityType, Embed, Intents
from requests import get
from discord.ext import commands
from datetime import datetime
from time import time as __, sleep as zzz
from re import findall
from keepalive import keep_alive  # Import the keep_alive function

def log(text, sleep=None): 
    print(f"[{datetime.utcfromtimestamp(__()).strftime('%Y-%m-%d %H:%M:%S')}] → {text}")
    if sleep: zzz(sleep)

class settings:
    token = os.getenv('DISCORD_BOT_TOKEN')  # Use environment variable for the bot token
    prefix = '!'  # Bot Prefix
    bot_status = '@saikitite Prefix: !'  # Bot Status
    intents = Intents.default()
    intents.message_content = True  # ✅ Fix: Allow bot to read messages
    client = commands.Bot(command_prefix=prefix, intents=intents)

log(f'Detected token: {settings.token}', 0.5)
log(f'Detected prefix: {settings.prefix}', 0.5)
log(f'Detected bot status: {settings.bot_status}', 0.5)

@settings.client.event
async def on_ready():
    log(f"Connected to {settings.client.user}", 0.5)
    await settings.client.change_presence(activity=Activity(type=ActivityType.watching, name=settings.bot_status))



@settings.client.command()
async def vc(ctx, cookie=None):
    if not cookie:
        await ctx.send(embed=Embed(title=":x: Missing Cookie", color=0xFF0000))
        log(f'User {ctx.author} tried to use {settings.prefix}vc but did not provide a cookie.')
        return

    await ctx.message.delete()
    headers = {"User-Agent": "Mozilla/5.0"}  # ✅ Fix: Add User-Agent header
    response = get('https://users.roblox.com/v1/users/authenticated', cookies={'.ROBLOSECURITY': cookie}, headers=headers)

    if response.status_code == 200 and '"id":' in response.text:
        log(f'User {ctx.author} used {settings.prefix}vc with a valid cookie.')
        embedVar = Embed(title=":white_check_mark: Valid Cookie", color=0x38d13b)
        embedVar.add_field(name="Passed Cookie: ", value='```                       Hidden                  ```', inline=False)
        embedVar.set_footer(text="Check your DMs for the cookie.")
        dm = await ctx.author.create_dm()
        await dm.send(embed=Embed(title=":white_check_mark: Cookie", description=f'```{cookie}```', color=0x38d13b))
        await ctx.send(embed=embedVar)
    elif response.status_code == 401:  # ✅ Fix: Check for 401 Unauthorized response
        log(f'User {ctx.author} used {settings.prefix}vc with an invalid cookie.')
        embedVar = Embed(title=":x: Invalid Cookie", color=0xFF0000)
        embedVar.add_field(name="Passed Cookie: ", value='```                       Hidden                  ```', inline=False)
        await ctx.send(embed=embedVar)
    else:
        log(f'User {ctx.author} used {settings.prefix}vc but Roblox returned an error.')
        embedVar = Embed(title=":x: Error", color=0xFFFF00)
        embedVar.add_field(name="Error: ", value=f'```{response.text}```', inline=False)
        await ctx.send(embed=embedVar)

@settings.client.command()
async def vcr(ctx, cookie=None):
    if not cookie:
        await ctx.send(embed=Embed(title=":x: Missing Cookie", color=0xFF0000))
        log(f'User {ctx.author} tried to use {settings.prefix}vcr but did not provide a cookie.')
        return

    await ctx.message.delete()
    headers = {"User-Agent": "Mozilla/5.0"}  # ✅ Fix: Add User-Agent header
    response = get('https://users.roblox.com/v1/users/authenticated', cookies={'.ROBLOSECURITY': cookie}, headers=headers)

    if response.status_code == 200 and '"id":' in response.text:
        log(f'User {ctx.author} used {settings.prefix}vcr with a valid cookie.')
        user_id = response.json().get('id', None)
        if user_id:
            robux_response = get(f'https://economy.roblox.com/v1/users/{user_id}/currency', cookies={'.ROBLOSECURITY': cookie}, headers=headers)
            if robux_response.status_code == 200:
                robux = robux_response.json().get('robux', 0)
                embedVar = Embed(title=":white_check_mark: Valid Cookie", color=0x38d13b)
                embedVar.add_field(name="Passed Cookie: ", value='```                       Hidden                  ```', inline=False)
                embedVar.add_field(name=":money_mouth: Robux", value=str(robux), inline=True)
                dm = await ctx.author.create_dm()
                await dm.send(embed=Embed(title=":white_check_mark: Cookie", description=f'```{cookie}```', color=0x38d13b))
                await ctx.send(embed=embedVar)
            else:
                embedVar = Embed(title=":x: Failed to retrieve Robux", color=0xFF0000)
                await ctx.send(embed=embedVar)
        else:
            embedVar = Embed(title=":x: Failed to retrieve user ID", color=0xFF0000)
            await ctx.send(embed=embedVar)
    elif response.status_code == 401:  # ✅ Fix: Check for 401 Unauthorized response
        log(f'User {ctx.author} used {settings.prefix}vcr with an invalid cookie.')
        embedVar = Embed(title=":x: Invalid Cookie", color=0xFF0000)
        embedVar.add_field(name="Passed Cookie: ", value='```                       Hidden                  ```', inline=False)
        await ctx.send(embed=embedVar)
    else:
        log(f'User {ctx.author} used {settings.prefix}vcr but Roblox returned an error.')
        embedVar = Embed(title=":x: Error", color=0xFFFF00)
        embedVar.add_field(name="Error: ", value=f'```{response.text}```', inline=False)
        await ctx.send(embed=embedVar)



@settings.client.command()
async def full(ctx, cookie=None):
    if not cookie:
        await ctx.send(embed=Embed(title=":x: Missing Cookie", description="", color=0xFF0000))
        return
    await ctx.message.delete()
    response = get('https://users.roblox.com/v1/users/authenticated',cookies={'.ROBLOSECURITY': cookie})
    hidden = '```                       Hidden                  ```'
    if '"id":' in response.text:
        user_id = response.json()['id']
        robux = get(f'https://economy.roblox.com/v1/users/{user_id}/currency',cookies={'.ROBLOSECURITY': cookie}).json()['robux']
        account_settings = get(f'https://www.roblox.com/my/settings/json',cookies={'.ROBLOSECURITY': cookie})
        account_name = account_settings.json()['Name']
        account_display_name = account_settings.json()['DisplayName']
        account_email_verified = account_settings.json()['IsEmailVerified']
        if bool(account_email_verified):
            account_email_verified = f'{account_email_verified} (`{account_settings.json()["UserEmail"]}`)'
        account_above_13 = account_settings.json()['UserAbove13']
        account_age_in_years = round(float(account_settings.json()['AccountAgeInDays']/365),2)
        account_has_premium = account_settings.json()['IsPremium']
        account_has_pin = account_settings.json()['IsAccountPinEnabled']
        account_2step = account_settings.json()['MyAccountSecurityModel']['IsTwoStepEnabled']
        embedVar = Embed(title=":white_check_mark: Valid Cookie", description="", color=0x38d13b)
        embedVar.add_field(name=":money_mouth: Robux", value=robux, inline=True)
        embedVar.add_field(name=":bust_in_silhouette: Account Name", value=f'{account_name} ({account_display_name})', inline=True)
        embedVar.add_field(name=":email: Email", value=account_email_verified, inline=True)
        embedVar.add_field(name=":calendar: Account Age", value=f'{account_age_in_years} years', inline=True)
        embedVar.add_field(name=":baby: Above 13", value=account_above_13, inline=True)
        embedVar.add_field(name=":star: Premium", value=account_has_premium, inline=True)
        embedVar.add_field(name=":key: Has PIN", value=account_has_pin, inline=True)
        embedVar.add_field(name=":lock: 2-Step Verification", value=account_2step, inline=True)
        await ctx.send(embed=embedVar)
    elif 'Unauthorized' in response.text:
        embedVar = Embed(title=":x: Invalid Cookie", description="", color=0xFF0000)
        embedVar.add_field(name="Passed Cookie: ", value='```                       Hidden                  ```', inline=False)
        await ctx.send(embed=embedVar)
    else:
        embedVar = Embed(title=":x: Error", description="", color=0xFFFF00)
        embedVar.add_field(name="Error: ", value='```'+response.text+'```', inline=False)
        await ctx.send(embed=embedVar)



        
def run_bot():
    settings.client.run(settings.token)

# Start the keep-alive server
keep_alive()

# Start the bot
run_bot()
