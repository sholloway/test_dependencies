import pytest

from test_dependencies.dependency_list_loader import DependencyListLoader

class TestDependencyListLoader:
  def test_raises_error_on_missing_file(self) -> None:
    dll = DependencyListLoader()
    with pytest.raises(FileNotFoundError) as e:
      dll.load(filepath='junk/path/dag.csv')

  def test_stuff(self) -> None:
    assert False