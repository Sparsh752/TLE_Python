import bot
import clist_api
import asyncio
import nest_asyncio
async def main():
    await bot.run_discord_bot()
if __name__ == '__main__':
    # a=clist_api.nextcontests()
    # print(a)
    nest_asyncio.apply()
    asyncio.run(main())      #initialising bot