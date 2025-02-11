import os
import discord
from discord import Activity, ActivityType, Embed, Intents
from requests import get
from discord.ext import commands
from datetime import datetime
from time import time as __, sleep as zzz
from re import findall
from keepalive import keep_alive


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
    headers = {"User-Agent": "Mozilla/5.0"}
    response = get('https://users.roblox.com/v1/users/authenticated', cookies={'.ROBLOSECURITY': cookie}, headers=headers)
    hidden = '```                       Hidden                  ```'

    if response.status_code == 200 and '"id":' in response.text:
        user_id = response.json()['id']
        embedVar = Embed(title=":white_check_mark: Valid Cookie", description="", color=0x38d13b)
        embedVar.add_field(name="Passed Cookie: ", value=hidden, inline=False)

        # Fetch Robux balance
        robux_response = get(f'https://economy.roblox.com/v1/users/{user_id}/currency', cookies={'.ROBLOSECURITY': cookie}, headers=headers)
        if robux_response.status_code == 200:
            robux = robux_response.json().get('robux', 0)
            embedVar.add_field(name=":money_mouth: Robux", value=str(robux), inline=True)
        else:
            embedVar.add_field(name=":money_mouth: Robux", value="Failed to retrieve", inline=True)

        # Fetch credit balance
        balance_credit_info = get(f'https://billing.roblox.com/v1/credit', cookies={'.ROBLOSECURITY': cookie}, headers=headers)
        if balance_credit_info.status_code == 200:
            balance_credit = balance_credit_info.json().get('balance', 0)
            balance_credit_currency = balance_credit_info.json().get('currencyCode', 'Unknown')
            embedVar.add_field(name=":moneybag: Balance", value=f'{balance_credit} {balance_credit_currency}', inline=True)
        else:
            embedVar.add_field(name=":moneybag: Balance", value="Failed to retrieve", inline=True)

        # Fetch account settings
        account_settings = get(f'https://www.roblox.com/my/settings/json', cookies={'.ROBLOSECURITY': cookie}, headers=headers)
        if account_settings.status_code == 200:
            account_data = account_settings.json()
            account_name = account_data.get('Name', 'Unknown')
            account_display_name = account_data.get('DisplayName', 'Unknown')
            account_email_verified = account_data.get('IsEmailVerified', False)
            account_email = account_data.get('UserEmail', 'Unknown') if account_email_verified else 'Not verified'
            account_above_13 = account_data.get('UserAbove13', False)
            account_age_in_days = account_data.get('AccountAgeInDays', 0)
            account_age_in_years = round(float(account_age_in_days / 365), 2)
            account_has_premium = account_data.get('IsPremium', False)
            account_has_pin = account_data.get('IsAccountPinEnabled', False)
            account_2step = account_data.get('MyAccountSecurityModel', {}).get('IsTwoStepEnabled', False)

            embedVar.add_field(name=":bust_in_silhouette: Account Name", value=f'{account_name} ({account_display_name})', inline=True)
            embedVar.add_field(name=":email: Email", value=account_email, inline=True)
            embedVar.add_field(name=":calendar: Account Age", value=f'{account_age_in_years} years', inline=True)
            embedVar.add_field(name=":baby: Above 13", value=account_above_13, inline=True)
            embedVar.add_field(name=":star: Premium", value=account_has_premium, inline=True)
            embedVar.add_field(name=":key: Has PIN", value=account_has_pin, inline=True)
            embedVar.add_field(name=":lock: 2-Step Verification", value=account_2step, inline=True)
        else:
            embedVar.add_field(name=":bust_in_silhouette: Account Name", value="Failed to retrieve", inline=True)

        # Fetch friends count
        friends_response = get('https://friends.roblox.com/v1/my/friends/count', cookies={'.ROBLOSECURITY': cookie}, headers=headers)
        if friends_response.status_code == 200:
            account_friends = friends_response.json().get('count', 0)
            embedVar.add_field(name=":busts_in_silhouette: Friends", value=account_friends, inline=True)
        else:
            embedVar.add_field(name=":busts_in_silhouette: Friends", value="Failed to retrieve", inline=True)

        # Fetch voice verification status
        voice_response = get('https://voice.roblox.com/v1/settings', cookies={'.ROBLOSECURITY': cookie}, headers=headers)
        if voice_response.status_code == 200:
            account_voice_verified = voice_response.json().get('isVerifiedForVoice', False)
            embedVar.add_field(name=":microphone2: Voice Verified", value=account_voice_verified, inline=True)
        else:
            embedVar.add_field(name=":microphone2: Voice Verified", value="Failed to retrieve", inline=True)

        # Fetch gamepasses worth
        gamepasses_response = get(f'https://www.roblox.com/users/inventory/list-json?assetTypeId=34&cursor=&itemsPerPage=100&pageNumber=1&userId={user_id}', cookies={'.ROBLOSECURITY': cookie}, headers=headers)
        if gamepasses_response.status_code == 200:
            check = findall(r'"PriceInRobux":(\d+)', gamepasses_response.text)
            account_gamepasses = str(sum([int(match) for match in check])) + ' R$'
            embedVar.add_field(name=":video_game: Gamepasses Worth", value=account_gamepasses, inline=True)
        else:
            embedVar.add_field(name=":video_game: Gamepasses Worth", value="Failed to retrieve", inline=True)

        # Fetch badges
        badges_response = get(f'https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges', cookies={'.ROBLOSECURITY': cookie}, headers=headers)
        if badges_response.status_code == 200:
            account_badges = ', '.join(findall(r'"name":"(.*?)"', badges_response.text))
            embedVar.add_field(name=":medal: Badges", value=account_badges, inline=True)
        else:
            embedVar.add_field(name=":medal: Badges", value="Failed to retrieve", inline=True)

        # Fetch transactions
        transactions_response = get(f'https://economy.roblox.com/v2/users/{user_id}/transaction-totals?timeFrame=Year&transactionType=summary', cookies={'.ROBLOSECURITY': cookie}, headers=headers)
        if transactions_response.status_code == 200:
            transactions_data = transactions_response.json()
            account_sales_of_goods = transactions_data.get('salesTotal', 0)
            account_purchases_total = abs(int(transactions_data.get('purchasesTotal', 0)))
            account_commissions = transactions_data.get('affiliateSalesTotal', 0)
            account_robux_purchased = transactions_data.get('currencyPurchasesTotal', 0)
            account_premium_payouts_total = transactions_data.get('premiumPayoutsTotal', 0)
            account_pending_robux = transactions_data.get('pendingRobuxTotal', 0)

            embedVar.add_field(name="↻ Transactions", value=':small_red_triangle_down: :small_red_triangle_down: :small_red_triangle_down:', inline=False)
            embedVar.add_field(name=":coin: Sales of Goods", value=account_sales_of_goods, inline=True)
            embedVar.add_field(name="💰 Premium Payouts", value=account_premium_payouts_total, inline=True)
            embedVar.add_field(name="📈 Commissions", value=account_commissions, inline=True)
            embedVar.add_field(name=":credit_card: Robux Purchased", value=account_robux_purchased, inline=True)
            embedVar.add_field(name="🚧 Pending", value=account_pending_robux, inline=True)
            embedVar.add_field(name=":money_with_wings: Overall", value=account_purchases_total, inline=True)
        else:
            embedVar.add_field(name="↻ Transactions", value="Failed to retrieve", inline=False)

        # Set thumbnail
        thumbnail_response = get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?size=48x48&format=png&userIds={user_id}')
        if thumbnail_response.status_code == 200:
            embedVar.set_thumbnail(url=thumbnail_response.json()['data'][0]['imageUrl'])

        # Send embed
        dm = await ctx.author.create_dm()
        await ctx.send(embed=embedVar)
        embedVar.add_field(name="Passed Cookie: ", value=cookie, inline=False)
        await dm.send(embed=embedVar)
        log(f'User {ctx.author} used {settings.prefix}full with a valid cookie.')

    elif response.status_code == 401:
        log(f'User {ctx.author} used {settings.prefix}full with an invalid cookie.')
        embedVar = Embed(title=":x: Invalid Cookie", description="", color=0xFF0000)
        embedVar.add_field(name="Passed Cookie: ", value=hidden, inline=False)
        await ctx.send(embed=embedVar)
    else:
        log(f'User {ctx.author} used {settings.prefix}full but Roblox returned a bad response.')
        embedVar = Embed(title=":x: Error", description="", color=0xFFFF00)
        embedVar.add_field(name="Error: ", value=f'```{response.text}```', inline=False)
        await ctx.send(embed=embedVar)


# Start bot
settings.client.run(settings.token)