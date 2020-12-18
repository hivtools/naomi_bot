import os
import aiohttp
import configparser

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

  repo_url = "/repos/mrc-ide/hintr"
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

  # Request review
  await gh.post(new_pr["url"] + "/requested_reviewers", data = {
    "reviewers": [
      "r-ash"
    ]
  })

  # Post link to new PR in a comment
  await gh.post(event.data["pull_request"]["comments_url"], data = {
    "body": "Thanks. Corresponding hintr PR at " + new_pr["html_url"]
  })


@routes.post("/naomi-bot/")
async def main(request):
  # read the GitHub webhook payload
  body = await request.read()

  # our authentication token and secret
  cfg = configparser.ConfigParser()
  cfg.read("app/vault_secrets.ini")
  secret = cfg.get("vault_secrets", "WEBHOOK_SECRET")
  oauth_token = cfg.get("vault_secrets", "GH_AUTH_TOKEN")

  # a representation of GitHub webhook event
  event = sansio.Event.from_http(request.headers, body, secret=secret)

  async with aiohttp.ClientSession() as session:
    gh = gh_aiohttp.GitHubAPI(session, "r-ash",
                              oauth_token=oauth_token)

    # call the appropriate callback for the event
    await router.dispatch(event, gh)

  # return a "Success"
  return web.Response(status=200)
  
@routes.get("/naomi-bot/")
async def test(request):
  # This GET endpoint isn't called by the bot, just using it for testing
  print("Test endoint running")
  return web.Response(status=200, text="Bot running")


if __name__ == "__main__":
  app = web.Application()
  app.add_routes(routes)
  port = os.environ.get("PORT")
  if port is not None:
    port = int(port)

  web.run_app(app, port=port)