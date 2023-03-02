import re

def get_version_number(text):
  match = re.search(r'Version: ([\d.]+)', text)
  if not match:
    raise Exception("Can't read version information")
  else:
    return(match.group(1))

def update_naomi_version(text, naomi_version):
  updated_text = re.sub(r'(\s*naomi \(>= )([\d.]+)', r'\g<1>' + naomi_version, text)
  if updated_text == text:
    raise Exception("Failed to update naomi version in text to " + naomi_version +
      " either can't find in file or version is same as what trying to update to")
  else:
    return(updated_text)

def update_docker_build(text, naomi_branch):
  updated_text = re.sub(r'(\s*git clone) (https://github.com/mrc-ide/naomi)', r'\g<1> --single-branch --branch ' + naomi_branch + r' \g<2>', text)
  if updated_text == text:
    raise Exception("Failed to update naomi branch in text to " + naomi_branch +
      " either can't find in file or branch is same as what trying to update to")
  else:
    return(updated_text)

def remove_branch_pin(text):
  updated_text = re.sub(r'git clone --single-branch --branch (.+) https://github.com/mrc-ide/naomi', r'git clone https://github.com/mrc-ide/naomi', text)
  if updated_text == text:
    raise Exception("Failed to remove branch pin either can't find in file or branch pin")
  else:
    return(updated_text)