import base64
from gidgethub import InvalidField


async def update_branch(gh, repo_url, naomi_branch):
  ## Create new branch
  ## Get master reference
  master = await gh.getitem(repo_url + "/git/ref/heads/master")
  print(master)
  print(master["object"]["sha"])
  new_branch = "naomi-" + naomi_branch
  print("creating " + new_branch)
  ## Create new reference pinned to master
  try:
    out = await gh.post(repo_url + "/git/refs", data = {
      "ref": "refs/heads/" + new_branch,
      "sha": master["object"]["sha"]
    })
  except InvalidField as e:
    message = e.args[0]
    if message == "Reference already exists": 
      await gh.patch(repo_url + "/git/refs/heads/" + new_branch, data = {
        "sha": master["object"]["sha"]
      })
      pass
    else:
      print("Can't recover")
      raise
  

  ## Make code change
  readme = await gh.getitem(repo_url + "/contents/README.md")
  print(readme)
  print(base64.b64decode(readme["content"]))
  content = base64.b64encode((bytes.decode(base64.b64decode(readme["content"])) + "\ntest edit readme").encode())
  print(content)

  await gh.put(repo_url + "/contents/README.md", data = {
    "message": "Update README",
    "content": str(content, "utf-8"),
    "sha": readme["sha"],
    "branch": new_branch
  })
 
  return("updating URL {} branch {}".format(repo_url, naomi_branch))