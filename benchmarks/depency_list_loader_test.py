from collections.abc import Callable
import pytest

import os
from pathlib import Path

from test_dependencies.dependency_list_loader import DependencyListLoader
  
class TestDependencyListLoader:
  @pytest.mark.benchmark(group="DependencyListLoader", disable_gc=True)
  def test_load_2k_member_dag(self, benchmark) -> None:
    loader = DependencyListLoader()
    filepath = os.path.join(Path.cwd(), 'examples/2k.csv')
    benchmark(loader.load, filepath)
  
  @pytest.mark.benchmark(group="DependencyListLoader", disable_gc=True)
  def test_load_100k_member_dag(self, benchmark) -> None:
    loader = DependencyListLoader()
    filepath = os.path.join(Path.cwd(), 'examples/100k.csv')
    benchmark(loader.load, filepath)