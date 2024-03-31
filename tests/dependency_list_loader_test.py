import pytest
import os
from pathlib import Path
from test_dependencies.item import Item
from test_dependencies.dependency_list_loader import DependencyListLoader, DependencyListNode

EXAMPLE_FILE = 'examples/dag_sample.csv'

@pytest.fixture
def example_dag() -> dict[str, DependencyListNode]:
  dll = DependencyListLoader()
  filepath = os.path.join(Path.cwd(), EXAMPLE_FILE)
  dag: dict[str, DependencyListNode] = dll.load(filepath)
  assert example_dag is not None 
  return dag 
  
class TestDependencyListLoader:
  def test_raises_error_on_missing_file(self) -> None:
    dll = DependencyListLoader()
    with pytest.raises(FileNotFoundError) as e:
      dll.load(filepath='junk/path/dag.csv')

  def test_dag_size(self, example_dag: dict[str, DependencyListNode]) -> None:
    assert len(example_dag) == 708, 'Expected 708 distinct assets.'

  def test_spot_check_dag(self, example_dag: dict[str, DependencyListNode]) -> None:
    assert 'AccountDataConstants' in example_dag
    assert example_dag['AccountDataConstants'].item.name == 'AccountDataConstants'
    assert example_dag['AccountDataConstants'].item.id == '01p0M000001HIboQAG'
    assert example_dag['AccountDataConstants'].item.type == 'ApexClass'
    assert len(example_dag['AccountDataConstants'].upstream) == 3
    assert Item('01p0M00000016viQAA', 'ADMUserTriggerHandler', 'ApexClass') in example_dag['AccountDataConstants'].upstream
    assert Item('01p0M00000016vjQAA', 'ContactTriggerHandler', 'ApexClass') in example_dag['AccountDataConstants'].upstream
    assert Item('01p0M000001LQF3QAO', 'AccountADMTriggerManager', 'ApexClass') in example_dag['AccountDataConstants'].upstream
    
    assert 'CSC_Constants' in example_dag
    assert example_dag['CSC_Constants'].item.name == 'CSC_Constants'
    assert example_dag['CSC_Constants'].item.id == '01p0M000001rtXBQAY'
    assert example_dag['CSC_Constants'].item.type == 'ApexClass'
    assert len(example_dag['CSC_Constants'].upstream) == 4
    assert Item('01p0M00000016arQAA', 'CSC_NewCompassController', 'ApexClass') in example_dag['CSC_Constants'].upstream
    assert Item('01p0M00000016asQAA', 'CSC_NewCompassControllerTest', 'ApexClass') in example_dag['CSC_Constants'].upstream
    assert Item('01p0M00000016utQAA', 'CSC_MyTrailsControllerTest', 'ApexClass') in example_dag['CSC_Constants'].upstream
    assert Item('01p0M00000016uzQAA', 'CSC_UserUtilsTest', 'ApexClass') in example_dag['CSC_Constants'].upstream

    assert 'ContactEmailOptOutUtil' in example_dag
    assert example_dag['ContactEmailOptOutUtil'].item.name == 'ContactEmailOptOutUtil'
    assert example_dag['ContactEmailOptOutUtil'].item.id == '01p0M000001LQuEQAW'
    assert example_dag['ContactEmailOptOutUtil'].item.type == 'ApexClass'
    assert len(example_dag['ContactEmailOptOutUtil'].upstream) == 1
    assert Item('01p0M000001LQuFQAW', 'ContactEmailOptOutUtilTest', 'ApexClass') in example_dag['ContactEmailOptOutUtil'].upstream