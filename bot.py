#!/usr/bin/env python
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main bot entry point"""
    logger.info("🚀 Starting AIGentArtBot...")
    
    # Initialize bot and dispatcher
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Include routers
    dp.include_router(router)
    
    # Start polling
    try:
        logger.info("✅ Bot is running! Press Ctrl+C to stop.")
        await dp.start_polling(bot, skip_updates=True)
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
    finally:
        await bot.session.close()
        logger.info("👋 Bot shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())
