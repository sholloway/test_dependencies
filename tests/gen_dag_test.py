import os 
from pathlib import Path

from test_dependencies.dag_generator import DAGGenerator
from test_dependencies.dependency_list_loader import DependencyListLoader, DependencyListNode
  
class TestGenDagFile:
  def test_gen_class_names(self, tmp_path: Path) -> None:
    dag_file = os.path.join(tmp_path, 'dag_file.csv')

    # 1. Make the file.
    gen = DAGGenerator()
    gen.generate(output_filepath=dag_file, num_hierarchies=5, max_distance=3)

    #2. Load it as an adjacency list.
    dll = DependencyListLoader()
    adjacency_list: dict[str, DependencyListNode] = dll.load(dag_file)
    assert len(adjacency_list) > 5