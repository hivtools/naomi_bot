import asyncio
import os
import aiohttp
from gidgethub.aiohttp import GitHubAPI

async def main():
  async with aiohttp.ClientSession() as session:
    gh = GitHubAPI(session, "r-ash", oauth_token=os.getenv("GH_AUTH"))
    await gh.post('/repos/r-ash/ws-install/issues',
          data={
            'title': 'Test issue creation',
            'body': 'Testing :)',
          })

loop = asyncio.get_event_loop()
loop.run_until_complete(main())