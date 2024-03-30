from collections.abc import Callable
import pytest

import os
from pathlib import Path

from test_dependencies.dependency_list_loader import DependencyListLoader

EXAMPLE_FILE = 'examples/dag_sample.csv'
  
class TestDependencyListLoader:
  @pytest.mark.benchmark(group="DependencyListLoader", disable_gc=True)
  def test_load_2k_member_dag(self, benchmark) -> None:
    loader = DependencyListLoader()
    filepath = os.path.join(Path.cwd(), EXAMPLE_FILE)
    benchmark(loader.load, filepath)