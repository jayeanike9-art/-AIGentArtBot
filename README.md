# 🤖 AIGentArtBot

An AI-powered Telegram bot for image generation, image conversion, and URL shortening.

## ✨ Features
- 🎨 AI Image Generation from text prompts
- 🖼️ Image Format Conversion (PNG, JPG, WEBP, etc.)
- 🔗 URL Shortening
- 📊 Usage Statistics
- 🎭 Multiple Art Styles

## 🚀 Deployment

### Prerequisites
- Python 3.11+
- Telegram Bot Token from @BotFather
- GitHub account
- Railway account

### Deploy on Railway

1. **Fork this repository** to your GitHub account

2. **Create a new bot** on Telegram via @BotFather
   - Get your BOT_TOKEN

3. **Deploy on Railway**
   - Sign in to [Railway.app](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repository
   - Add environment variables:
     - `BOT_TOKEN`: Your Telegram bot token
   - Click "Deploy"

4. **Your bot is live!** 🎉

## 🛠️ Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/AIGentArtBot.git
cd AIGentArtBot

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your BOT_TOKEN
echo "BOT_TOKEN=your_bot_token_here" > .env

# Run the bot
python bot.py
