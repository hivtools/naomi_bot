import pytest
import os

import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
from naomi_bot import update_branch

def test_update_branch():
  oauth_token = os.environ.get("GH_AUTH")
  async with aiohttp.ClientSession() as session:
    gh = gh_aiohttp.GitHubAPI(session, "r-ash",
                              oauth_token=oauth_token)

    # call the appropriate callback for the event
    await router.dispatch(event, gh)


  assert update_branch.update_branch(gh, "/repos/r-ash/ws-install", "v0.0.50") == "updating version test1 branch test2"