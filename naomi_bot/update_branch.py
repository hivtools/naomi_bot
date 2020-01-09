import tempfile
from git import Repo

def update_branch(gh, repo_url, naomi_branch):
  ## Clone the repo
  ##repo = Repo
  ##Repo.clone_from(git_url, repo_dir)

  ## Create new branch


  ## Make code change
  readme = gh.get(repo_url + "/contents/README.md")
  print(readme)
  content = readme["content"] + "test edit readme"

  gh.put(repo_url + "/contents/README.md", data = {
    "message" = "Update README",
    "content" = content,
    "sha" = readme["sha"],
    "branch" = "naomi " + naomi_branch
  })
 
  return("updating version {} branch {}".format(naomi_version, naomi_branch))