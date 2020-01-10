import os

import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
from .update_branch import update_branch
from .version import get_version_number
from .utils import text_from_base64

router = routing.Router()
routes = web.RouteTableDef()

@router.register("pull_request", action="opened")
async def new_pr_event(event, gh, *args, **kwargs):
  """ Whenever a PR is opening in naomi, open corresponding PR in hintr"""
  # url = event.data["issue"]["comments_url"]
  # Hardcode the URL eventually this will be hintr
  repo_url = "/repos/r-ash/ws-install"
  naomi_branch = event.data["pull_request"]["head"]["ref"]
  print("Handling new PR for naomi branch " + naomi_branch)
  
  description = await gh.getitem(event.data["pull_request"]["head"]["repo"]["url"] + 
    "/contents/DESCRIPTION" + "?ref=" + naomi_branch
  )
  description_text = text_from_base64(description["content"])
  version_number = get_version_number(description_text)
  new_branch = "naomi-" + version_number

  await update_branch(gh, repo_url, version_number, naomi_branch, new_branch)

  # Create pull request
  new_pr = await gh.post(repo_url + "/pulls", data = {
    "title": new_branch,
    "body": 'Automatically created PR from new naomi PR "' + 
      event.data["pull_request"]["title"] + '" - ' + event.data["pull_request"]["html_url"],
    "head": new_branch,
    "base": "master"
  })

  # Post link to new PR in a comment
  await gh.post(event.data["pull_request"]["comments_url"], data = {
    "body": "Thanks. Corresponding hintr PR at " + new_pr["html_url"]
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
    naomi_branch = "new-branch"
    version_number = "0.0.50.1"
    new_branch = "naomi-" + version_number
    await update_branch(gh, "/repos/r-ash/ws-install", version_number, naomi_branch, new_branch)
  return web.Response(status=200, text="Hello")


if __name__ == "__main__":
  app = web.Application()
  app.add_routes(routes)
  port = os.environ.get("PORT")
  if port is not None:
    port = int(port)

  web.run_app(app, port=port)