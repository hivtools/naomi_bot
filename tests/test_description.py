import pytest

from naomi_bot import description

def test_get_version_number():
  description_text = """
  Package: naomi
  Title: Naomi model for subnational HIV estimates
  Version: 0.0.49
  Authors@R:

  """
  assert description.get_version_number(description_text) == "0.0.49"

  # Missing version
  with pytest.raises(Exception):
    description.get_version_number("test")
