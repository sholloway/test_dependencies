
from test_dependencies.change_list_loader import ChangeListLoader
from test_dependencies.dependency_list_loader import DependencyListLoader, DependencyListNode
from test_dependencies.apex_test_selector import ApexTestSelector
from test_dependencies.options_processor import OptionsProcessor

class App:
  def __init__(self) -> None:
    self._op = OptionsProcessor()
    self._dll = DependencyListLoader()
    self._cll = ChangeListLoader()
    self._selector = ApexTestSelector()
    
  def run(self) -> None:
    options = self._op.process()
    
    # 1. Load the Dependencies provided by Salesforce into an adjacent list.
    dependency_list: dict[str, DependencyListNode] = self._dll.load(filepath=options['dependency_list'])

    # 2. Load the list of changed Apex classes into memory as a list.
    changed_list: list[str] = self._cll.load(filepath=options['changed_list'])

    # 3. Find all tests for the specified depth.
    tests_to_run, missing_items = self._selector.select(
      dependency_graph = dependency_list, 
      changed_list = changed_list,
      maximum_distance = options['degrees']
    )

    # 4. Calculate the Statistics
    print(f'Number of Tests in DAG: {self._dll.num_tests:,}')
    print(f'Number of Apex Classes in DAG: {self._dll.num_apex_classes:,}')
    print(f'Number of Tests to Run: {len(tests_to_run)}git ')
    print(f'Number of Missing Items in DAG: {len(missing_items)}')
    print(f'Runing {len(tests_to_run)/self._dll.num_tests * 100:.2f} percent of all tests.')

    # 5. Write the identified tests to run to STDOUT.
    print('\nTests to Run')
    for test in tests_to_run:
      print(test)

    if len(missing_items) > 0:
      print('\nMissing Items')
      for missing in missing_items:
        print(missing)