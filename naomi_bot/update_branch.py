import base64
from gidgethub import InvalidField


async def update_branch(gh, repo_url, naomi_branch, new_branch):
  ## Create new branch
  ## Get master reference
  master = await gh.getitem(repo_url + "/git/ref/heads/master")

  ## Create new reference pinned to master
  try:
    await gh.post(repo_url + "/git/refs", data = {
      "ref": "refs/heads/" + new_branch,
      "sha": master["object"]["sha"]
    })
    print("Created " + new_branch + " at master ref " + master["object"]["sha"])
  except InvalidField as e:
    message = e.args[0]
    if message == "Reference already exists": 
      await gh.patch(repo_url + "/git/refs/heads/" + new_branch, data = {
        "sha": master["object"]["sha"]
      })
      print("Updated " + new_branch + " to master ref " + master["object"]["sha"])
      pass
    else:
      print("Can't set " + new_branch + " to master ref " + 
        master["object"]["sha"] + ", branch is ahead of master")
      raise
  

  ## Make code change
  readme = await gh.getitem(repo_url + "/contents/README.md")
  content_readable = bytes.decode(base64.b64decode(readme["content"])) + "\ntest edit readme"
  print("Updating content to " + content_readable)
  content = base64.b64encode((content_readable).encode())

  await gh.put(repo_url + "/contents/README.md", data = {
    "message": "Update README",
    "content": str(content, "utf-8"),
    "sha": readme["sha"],
    "branch": new_branch
  })
 
  return("Updating URL {} branch {}".format(repo_url, naomi_branch))