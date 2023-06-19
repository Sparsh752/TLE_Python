import bot
import asyncio
import nest_asyncio
# Driver Code. Made async to run the bot asynchronously
async def main():
    await bot.run_discord_bot()
if __name__ == '__main__':
    # To run the bot asynchronously we need to use nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())      