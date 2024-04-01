import os
from pathlib import Path
import pytest

from test_dependencies.change_list_loader import ChangeListLoader
from test_dependencies.dependency_list_loader import DependencyListLoader, DependencyListNode
from test_dependencies.apex_test_selector import ApexTestSelector

EXAMPLE_DAG_FILE = 'examples/2k.csv'
EXAMPLE_CHANGE_LIST = 'examples/2k_changed_list.txt'

@pytest.fixture
def example_dag() -> dict[str, DependencyListNode]:
  dll = DependencyListLoader()
  filepath = os.path.join(Path.cwd(), EXAMPLE_DAG_FILE)
  dag: dict[str, DependencyListNode] = dll.load(filepath)
  assert example_dag is not None 
  return dag 

@pytest.fixture
def example_change_list() -> list[str]:
  change_list_loader = ChangeListLoader()
  filepath = os.path.join(Path.cwd(), EXAMPLE_CHANGE_LIST)
  changed_list = change_list_loader.load(filepath)
  assert changed_list is not None
  return changed_list

class TestDistanceMatrixBuilder:
  def test_happy_path(
    self, 
    example_dag: dict[str, DependencyListNode], 
    example_change_list: list[str]
  ) -> None:
    selector = ApexTestSelector()
    tests_to_run, missing_items = selector.select(example_dag, example_change_list, maximum_distance = 1)
    assert len(tests_to_run) == 7
    assert len(missing_items) == 0

  def test_missing_data(self, 
    example_dag: dict[str, DependencyListNode], 
    example_change_list: list[str]
  ) -> None:
    # The 2k sized sample file has references to classes that aren't present.
    # When a class is encountered that cannot be found, it is skipped but recorded.
    selector = ApexTestSelector()
    tests_to_run, missing_items = selector.select(example_dag, example_change_list, maximum_distance = 2)
    assert len(tests_to_run) == 8
    assert len(missing_items) == 5