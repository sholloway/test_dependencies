
from test_dependencies.change_list_loader import ChangeListLoader
from test_dependencies.dependency_list_loader import DependencyListLoader, DependencyListNode, AdjacencyListType
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
    dependency_list: AdjacencyListType = self._dll.load(filepath=options['dependency_list'])

    # 2. Load the list of changed Apex classes into memory as a list.
    changed_list: list[str] = self._cll.load(filepath=options['changed_list'])

    # 3. Find all tests for the specified depth.
    tests_to_run, missing_items = self._selector.select(
      dependency_graph = dependency_list, 
      changed_list = changed_list,
      maximum_distance = options['degrees']
    )

    # 4. Calculate the Statistics
    table_format = "| {:<22} | {:<40} |"
    header = table_format.format('Metric', 'Value')
    boarder = '|' + '-'*24 + '|' + '-'*43
  
    print(boarder)
    print(header)
    print(boarder)
    print(table_format.format('Changed Files', f'{len(changed_list):,}'))
    print(table_format.format('Tests in DAG', f'{self._dll.num_tests:,}'))
    print(table_format.format('Apex Classes in DAG', f'{self._dll.num_apex_classes:,}'))
    print(table_format.format('Tests to Run', f'{len(tests_to_run):,}'))
    print(table_format.format('Missing Items in DAG', f'{len(missing_items):,}'))
    print(boarder)
  
    print(f'\nIdentified {len(tests_to_run)/self._dll.num_tests * 100:.2f} percent of all tests.')

    # 5. Write the identified tests to run to STDOUT.
    print('\nTests to Run')
    for test in tests_to_run:
      print(test)

    if len(missing_items) > 0:
      print('\nMissing Items')
      for missing in missing_items:
        print(missing)