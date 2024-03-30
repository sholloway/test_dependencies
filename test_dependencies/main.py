
from test_dependencies.change_list_loader import ChangeListLoader
from test_dependencies.dependency_list_loader import DependencyListLoader, DependencyListNode
from test_dependencies.distance_matrix_builder import DistanceMatrixBuilder
from test_dependencies.options_processor import OptionsProcessor

def main() -> None:
  op = OptionsProcessor()
  options = op.process()
  
  # 1. Load the Dependencies provided by Salesforce into an adjacent list.
  dll = DependencyListLoader()
  dependency_list: dict[str, DependencyListNode] = dll.load(filepath=options['dependency_list'])

  # 2. Load the list of changed Apex classes into memory as a list.
  cll = ChangeListLoader()
  changed_list: list[str] = cll.load(filepath=options['changed_list'])

  # 3. Build the distance matrix for the specified depth.
  dmb = DistanceMatrixBuilder()
  distance_matrix: dict[str, dict[int, list[str]]] = dmb.build(
    dependency_graph = dependency_list, 
    changed_list = changed_list,
    maximum_distance = options['degrees']
  )

  # 4. Write the identified tests to run to STDOUT.
  print(distance_matrix)
  print('Not done yet. :P')