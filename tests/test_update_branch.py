import pytest
from naomi_bot import update_branch

def test_update_branch():
  assert update_branch.update_branch("test1", "test2") == "updating version test1 branch test2"