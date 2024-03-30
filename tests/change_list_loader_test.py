import os
from pathlib import Path
import pytest

from test_dependencies.change_list_loader import ChangeListLoader

EXAMPLE_CHANGE_LIST = 'examples/changed_list.txt'

@pytest.fixture
def change_list_loader() -> ChangeListLoader:
  return ChangeListLoader()

@pytest.fixture
def example_change_list(change_list_loader: ChangeListLoader) -> list[str]:
  filepath = os.path.join(Path.cwd(), EXAMPLE_CHANGE_LIST)
  changed_list = change_list_loader.load(filepath)
  assert changed_list is not None
  return changed_list

class TestChangeListLoader:
  def test_raises_error_on_missing_file(self, change_list_loader: ChangeListLoader) -> None:
    with pytest.raises(FileNotFoundError) as e:
      change_list_loader.load(filepath='junk/path/changes.txt')

  def test_loaded_list_size(self, example_change_list: list[str]) -> None:
    assert len(example_change_list) == 3
    assert 'SfdcPublishQuoteDao' in example_change_list
    assert 'CSC_TestDataFactory' in example_change_list
    assert 'CSC_WaveService' in example_change_list