import discord
from discord.ext import tasks
import aiohttp
import asyncio
import os
from datetime import datetime

# Bot configuration
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN', 'YOUR_DISCORD_BOT_TOKEN_HERE')
UPDATE_INTERVAL = 60  # Update every 5 minutes (300 seconds)

# Initialize bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

class HypePriceTracker:
    def __init__(self):
        self.price = 0.0
        self.change_24h = 0.0
        self.last_update = None
    
    async def fetch_price(self):
        """Fetch HYPE price from CoinGecko API"""
        try:
            async with aiohttp.ClientSession() as session:
                # Using CoinGecko API for Hyperliquid token
                url = 'https://api.coingecko.com/api/v3/simple/price'
                params = {
                    'ids': 'hyperliquid',  # CoinGecko ID for HYPE
                    'vs_currencies': 'usd',
                    'include_24hr_change': 'true'
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'hyperliquid' in data:
                            self.price = data['hyperliquid']['usd']
                            self.change_24h = data['hyperliquid'].get('usd_24h_change', 0.0)
                            self.last_update = datetime.now()
                            return True
                    return False
        except Exception as e:
            print(f"Error fetching price: {e}")
            return False
    
    def get_status_text(self):
        """Generate status text for the bot"""
        arrow = "📈" if self.change_24h >= 0 else "📉"
        return f"HYPE ${self.price:.2f} {arrow}{abs(self.change_24h):.1f}%"
    
    def get_embed(self):
        """Create a Discord embed matching the style of your image"""
        # Determine color based on 24h change
        color = 0x2ecc71 if self.change_24h >= 0 else 0xe74c3c  # Green or Red
        
        embed = discord.Embed(
            title="🔥 HYPE Price Monitor",
            color=color,
            timestamp=self.last_update
        )
        
        # Price field
        embed.add_field(
            name="💰 Current Price",
            value=f"**${self.price:.2f}**",
            inline=True
        )
        
        # 24h change field
        change_emoji = "🟢" if self.change_24h >= 0 else "🔴"
        change_symbol = "+" if self.change_24h >= 0 else ""
        embed.add_field(
            name="📊 24h Change",
            value=f"{change_emoji} **{change_symbol}{self.change_24h:.1f}%**",
            inline=True
        )
        
        embed.set_footer(text="Updates every 5 minutes")
        
        return embed

# Initialize price tracker
tracker = HypePriceTracker()
message_id = None
channel_id = None

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'Bot is in {len(client.guilds)} server(s)')
    update_price.start()

@tasks.loop(seconds=UPDATE_INTERVAL)
async def update_price():
    """Update the price and bot status"""
    global message_id, channel_id
    
    success = await tracker.fetch_price()
    
    if success:
        # Update bot nickname to show price
        for guild in client.guilds:
            try:
                await guild.me.edit(nick=f"HYPE ${tracker.price:.2f}")
            except discord.Forbidden:
                print(f"Cannot change nickname in {guild.name} - missing permissions")
            except Exception as e:
                print(f"Error updating nickname: {e}")
        
        # Update bot status to show 24h change (matching SOL style)
        arrow = "↗ " if tracker.change_24h >= 0 else "↘ "
        status_text = f"{arrow}{abs(tracker.change_24h):.1f}% 24h"
        
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=status_text
            )
        )
        print(f"Updated: HYPE ${tracker.price:.2f} | {status_text}")
        
        # If you want to post in a channel, uncomment below:
        # if channel_id:
        #     channel = client.get_channel(channel_id)
        #     if channel:
        #         embed = tracker.get_embed()
        #         if message_id:
        #             try:
        #                 msg = await channel.fetch_message(message_id)
        #                 await msg.edit(embed=embed)
        #             except:
        #                 msg = await channel.send(embed=embed)
        #                 message_id = msg.id
        #         else:
        #             msg = await channel.send(embed=embed)
        #             message_id = msg.id

@client.event
async def on_message(message):
    """Handle commands"""
    if message.author == client.user:
        return
    
    # Command to show current price
    if message.content.lower() == '!hype':
        await tracker.fetch_price()
        embed = tracker.get_embed()
        await message.channel.send(embed=embed)
    
    # Command to set update channel
    if message.content.lower() == '!hype setup':
        global channel_id, message_id
        channel_id = message.channel.id
        message_id = None
        await message.channel.send("✅ This channel will now receive HYPE price updates!")

# Run the bot
if __name__ == '__main__':
    if DISCORD_TOKEN == 'YOUR_DISCORD_BOT_TOKEN_HERE':
        print("⚠️  ERROR: Please set your Discord bot token in the script!")
        print("Replace 'YOUR_DISCORD_BOT_TOKEN_HERE' with your actual bot token")
    else:
        client.run(DISCORD_TOKEN)
