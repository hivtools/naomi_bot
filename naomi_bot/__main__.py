import os

import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
from update_branch import update_branch

router = routing.Router()
routes = web.RouteTableDef()

@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
  """ Whenever an issue is opened, open another one in a different repo"""
  # url = event.data["issue"]["comments_url"]
  ## Hardcode the URL eventually this will be hintr
  update_branch("test", "test_branch")
  url = "/repos/r-ash/ws-install/pulls"
  data = {
    "title": "Test issue",
    "body": "Test issue created by a bot",
    "head": "test-branch",
    "base": "master"
  }
  await gh.post(url, data=data)

@routes.post("/")
async def main(request):
  # read the GitHub webhook payload
  body = await request.read()

  # our authentication token and secret
  secret = os.environ.get("GH_SECRET")
  oauth_token = os.environ.get("GH_AUTH")

  # a representation of GitHub webhook event
  event = sansio.Event.from_http(request.headers, body, secret=secret)

  async with aiohttp.ClientSession() as session:
    gh = gh_aiohttp.GitHubAPI(session, "r-ash",
                              oauth_token=oauth_token)

    # call the appropriate callback for the event
    await router.dispatch(event, gh)

  # return a "Success"
  return web.Response(status=200)


if __name__ == "__main__":
  app = web.Application()
  app.add_routes(routes)
  port = os.environ.get("PORT")
  if port is not None:
    port = int(port)

  web.run_app(app, port=port)