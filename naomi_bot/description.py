import re

def get_version_number(text):
  match = re.search(r'Version: ([\d.]+)', text)
  if not match:
    raise Exception("Can't read version information")
  else:
    return match.group(1)