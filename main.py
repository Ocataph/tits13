import os
import discord
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
        await ctx.send(embed=Embed(title=":x: Missing Cookie", color=0xFF0000))
        log(f'User {ctx.author} tried to use {settings.prefix}full but did not provide a cookie.')
        return

    await ctx.message.delete()
    headers = {"User-Agent": "Mozilla/5.0"}
    cookies = {'.ROBLOSECURITY': cookie}

    response = get('https://users.roblox.com/v1/users/authenticated', cookies=cookies, headers=headers)
    
    if response.status_code == 200 and '"id":' in response.text:
        user_data = response.json()
        user_id = user_data.get('id', None)
        
        if not user_id:
            await ctx.send(embed=Embed(title=":x: Failed to retrieve user ID", color=0xFF0000))
            return

        log(f'User {ctx.author} used {settings.prefix}full with a valid cookie.')

        # Get Robux balance
        robux_response = get(f'https://economy.roblox.com/v1/users/{user_id}/currency', cookies=cookies, headers=headers)
        robux = robux_response.json().get('robux', 0) if robux_response.status_code == 200 else "N/A"

        # Get Credit balance
        credit_response = get(f'https://billing.roblox.com/v1/credit', cookies=cookies, headers=headers)
        if credit_response.status_code == 200:
            credit_data = credit_response.json()
            balance_credit = credit_data.get('balance', "N/A")
            balance_currency = credit_data.get('currencyCode', "N/A")
        else:
            balance_credit, balance_currency = "N/A", "N/A"

        # Get Account settings
        account_response = get('https://www.roblox.com/my/settings/json', cookies=cookies, headers=headers)
        if account_response.status_code == 200:
            account_data = account_response.json()
            account_name = account_data.get('Name', "N/A")
            account_display_name = account_data.get('DisplayName', "N/A")
            account_email_verified = account_data.get('IsEmailVerified', False)
            account_email = account_data.get("UserEmail", "Hidden") if account_email_verified else "Not Verified"
            account_above_13 = account_data.get('UserAbove13', "N/A")
            account_age = round(account_data.get('AccountAgeInDays', 0) / 365, 2)
            account_has_premium = account_data.get('IsPremium', False)
            account_has_pin = account_data.get('IsAccountPinEnabled', False)
            account_2step = account_data.get('IsTwoStepVerificationEnabled', False)
        else:
            account_name, account_display_name, account_email = "N/A", "N/A", "N/A"
            account_above_13, account_age, account_has_premium = "N/A", "N/A", "N/A"
            account_has_pin, account_2step = "N/A", "N/A"

        # Get Friends count
        friends_response = get('https://friends.roblox.com/v1/my/friends/count', cookies=cookies, headers=headers)
        friends_count = friends_response.json().get('count', 0) if friends_response.status_code == 200 else "N/A"

        # Get Voice verification
        voice_response = get('https://voice.roblox.com/v1/settings', cookies=cookies, headers=headers)
        voice_verified = voice_response.json().get('isVerifiedForVoice', False) if voice_response.status_code == 200 else "N/A"

        # Construct Embed
        embedVar = Embed(title=":white_check_mark: Valid Cookie", color=0x38d13b)
        embedVar.add_field(name="Passed Cookie", value="```Hidden```", inline=False)
        embedVar.add_field(name=":money_mouth: Robux", value=str(robux), inline=True)
        embedVar.add_field(name=":moneybag: Balance", value=f"{balance_credit} {balance_currency}", inline=True)
        embedVar.add_field(name=":bust_in_silhouette: Account Name", value=f"{account_name} ({account_display_name})", inline=True)
        embedVar.add_field(name=":email: Email", value=account_email, inline=True)
        embedVar.add_field(name=":calendar: Account Age", value=f"{account_age} years", inline=True)
        embedVar.add_field(name=":baby: Above 13", value=str(account_above_13), inline=True)
        embedVar.add_field(name=":star: Premium", value=str(account_has_premium), inline=True)
        embedVar.add_field(name=":key: Has PIN", value=str(account_has_pin), inline=True)
        embedVar.add_field(name=":lock: 2-Step Verification", value=str(account_2step), inline=True)
        embedVar.add_field(name=":busts_in_silhouette: Friends", value=str(friends_count), inline=True)
        embedVar.add_field(name=":microphone2: Voice Verified", value=str(voice_verified), inline=True)

        # Send Embed
        await ctx.send(embed=embedVar)
    elif response.status_code == 401:
        log(f'User {ctx.author} used {settings.prefix}full with an invalid cookie.')
        await ctx.send(embed=Embed(title=":x: Invalid Cookie", color=0xFF0000))
    else:
        log(f'User {ctx.author} used {settings.prefix}full but Roblox returned an error.')
        await ctx.send(embed=Embed(title=":x: Error", description=f"```{response.text}```", color=0xFFFF00))

        
def run_bot():
    settings.client.run(settings.token)

# Start the keep-alive server
keep_alive()

# Start the bot
run_bot()
