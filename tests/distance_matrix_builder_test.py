import os
from pathlib import Path
import pytest

from test_dependencies.change_list_loader import ChangeListLoader
from test_dependencies.dependency_list_loader import DependencyListLoader, DependencyListNode
from test_dependencies.distance_matrix_builder import DistanceMatrixBuilder

EXAMPLE_DAG_FILE = 'examples/dag_sample.csv'
EXAMPLE_CHANGE_LIST = 'examples/changed_list.txt'

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
  def test_stuff(
    self, 
    example_dag: dict[str, DependencyListNode], 
    example_change_list: list[str]
  ) -> None:
    dmb = DistanceMatrixBuilder()
    distance_matrix = dmb.build(example_dag, example_change_list, maximum_distance=1)
    assert distance_matrix is not None
    print(distance_matrix)
    assert False

  def test_gen_data(self) -> None:
    maximum_distance: int = 5
    current_item = None 
    for current_distance in range(1, maximum_distance+1):
      if current_distance == maximum_distance:
        #End of the chain, so create a test.