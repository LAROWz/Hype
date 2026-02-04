# 🔥 HYPE Price Discord Bot - Setup Guide

This bot monitors the $HYPE (Hyperliquid) token price and displays it in your Discord server, matching the style of your existing crypto widgets.

## Features
  ✅ Updates HYPE price every minute   
  ✅ Shows 24-hour price change percentage  
  ✅ Bot status displays current price in the member list  
✅ Optional: Post price updates in a channel  
✅ Command: `!hype` to check price anytime  

---

## 📋 Prerequisites
- Python 3.8 or higher
- A Discord account with server admin permissions

---

## 🚀 Setup Instructions

### Step 1: Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "HYPE Price Bot")
3. Go to the "Bot" tab on the left
4. Click "Add Bot" and confirm
5. Under "Privileged Gateway Intents", enable:
   - ✅ Message Content Intent
   - ✅ Server Members Intent (optional)
6. Click "Reset Token" and copy your bot token (keep this secret!)

### Step 2: Invite Bot to Your Server

1. Go to the "OAuth2" → "URL Generator" tab
2. Select scopes:
   - ✅ `bot`
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ View Channels
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

### Step 3: Install Python Dependencies

Open terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install discord.py aiohttp
```

### Step 4: Configure the Bot

1. Open `hype_price_bot.py` in a text editor
2. Find line 9: `DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN_HERE'`
3. Replace `YOUR_DISCORD_BOT_TOKEN_HERE` with your actual bot token from Step 1
4. Save the file

### Step 5: Run the Bot

```bash
python hype_price_bot.py
```

You should see:
```
HYPE Price Bot#1234 has connected to Discord!
Bot is in 1 server(s)
```

The bot will now:
- Update its status every minute with the current HYPE price
- Appear in your server's member list showing the price

---

## 💬 Optional: Enable Channel Updates

If you want the bot to post price updates in a specific channel:

1. In `hype_price_bot.py`, find the section around line 99-110 (the commented code)
2. Uncomment those lines (remove the `#` at the start)
3. In Discord, go to the channel where you want updates
4. Type: `!hype setup`
5. The bot will now edit a single message in that channel with price updates

---

## 🎮 Commands

- `!hype` - Show current HYPE price with an embed
- `!hype setup` - Set current channel for auto-updates (if enabled)

---

## ⚙️ Customization

### Change Update Interval
Edit line 10 in `hype_price_bot.py`:
```python
UPDATE_INTERVAL = 300  # 300 seconds = 5 minutes
```

### Change Token
If you want to track a different token, edit the CoinGecko ID on line 27:
```python
'ids': 'hyperliquid',  # Change this to another CoinGecko token ID
```

Find token IDs at: https://www.coingecko.com/

---

## 🔧 Troubleshooting

**Bot doesn't appear online:**
- Check your bot token is correct
- Make sure Message Content Intent is enabled in Discord Developer Portal

**Price not updating:**
- Check your internet connection
- CoinGecko API may have rate limits (free tier allows ~50 calls/minute)
- Try increasing UPDATE_INTERVAL if you get rate limited

**Bot crashes:**
- Make sure all dependencies are installed
- Check Python version (needs 3.8+)

---

## 🎨 Matching Your Discord Theme

The bot's embed colors automatically match price changes:
- 🟢 Green when price is up
- 🔴 Red when price is down

The status shown in the member list displays: `HYPE $XX.XX 📈/📉 X.X%`

---

## 🌐 Running 24/7

To keep the bot running continuously:

**Option 1: VPS/Cloud Server**
- Use a service like DigitalOcean, AWS, or Heroku
- Upload the files and run the bot there

**Option 2: Your PC with Background Process**
- Windows: Use `pythonw hype_price_bot.py` or Task Scheduler
- Linux/Mac: Use `nohup python hype_price_bot.py &` or create a systemd service

**Option 3: Free Hosting**
- Railway.app, Render.com, or fly.io offer free tiers for hosting bots

---

## 📝 Notes

- The bot uses CoinGecko's free API (no API key needed)
- HYPE = Hyperliquid token
- Data updates every 5 minutes by default
- Bot shows in your member list like other bots

---

## 🆘 Need Help?

If you encounter issues:
1. Check the console output for error messages
2. Verify all setup steps were completed
3. Make sure the bot has proper permissions in your Discord server

Enjoy your HYPE price monitor! 🚀
