import os

import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
from .update_branch import update_branch
from .description import get_version_number

router = routing.Router()
routes = web.RouteTableDef()

@router.register("pull_request", action="opened")
async def new_pr_event(event, gh, *args, **kwargs):
  """ Whenever a PR is opening in naomi, open corresponding PR in hintr"""
  # url = event.data["issue"]["comments_url"]
  # Hardcode the URL eventually this will be hintr
  repo_url = "/repos/r-ash/ws-install"
  naomi_branch = event["pull_request"]["head"]["ref"]
  print(naomi_branch)
  # TODO: Use version number for new branch name not the naomi_branch name
  description = await gh.getitem(repo_url + "/contents/DESCRIPTION")
  description_text = bytes.decode(base64.b64decode(readme["content"]))
  version_number = get_version_number(description_text)
  new_branch = "naomi-" + naomi_branch
  await update_branch(gh, repo_url, naomi_branch, new_branch)

  # Create pull request
  await gh.post(repo_url + "/pulls", data={
    "title": "Test issue",
    "body": "Test issue created by a bot",
    "head": "test-branch",
    "base": new_branch
  })

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
  
@routes.get("/")
async def test(request):
  # This GET endpoint isn't called by the bot, just using it for testing
  oauth_token = os.environ.get("GH_AUTH")
  async with aiohttp.ClientSession() as session:
    gh = gh_aiohttp.GitHubAPI(session, "r-ash",
                              oauth_token=oauth_token)
    naomi_branch = "v0.0.50"
    await update_branch(gh, "/repos/r-ash/ws-install", naomi_branch)
  return web.Response(status=200, text="Hello")


if __name__ == "__main__":
  app = web.Application()
  app.add_routes(routes)
  port = os.environ.get("PORT")
  if port is not None:
    port = int(port)

  web.run_app(app, port=port)