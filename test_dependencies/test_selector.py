
from test_dependencies.item import Item
from test_dependencies.dependency_list_loader import DependencyListNode

MissingDAGNode = DependencyListNode(
  item = Item(id = '', name='MISSING', type=''), 
  upstream=set()
)



class TestSelector:
  def __init__(self) -> None:
    pass

  def select(
    self, 
    dependency_graph: dict[str, DependencyListNode], 
    changed_list: list[str], 
    maximum_distance: int
  ) -> set[str]:
    tests = set[str]()
    missing_items = set[str]()
    for changed_item_name in changed_list:
      if changed_item_name.upper().endswith('TEST'):
        # If the changed item is a test, then just add it to the list of 
        # tests to run.
        tests.add(changed_item_name)
      else:
        self.find_upstream(
          changed_item_name, 
          dependency_graph, 
          tests,
          missing_items,
          1, 
          maximum_distance
        )
    return tests, missing_items
  
  def find_upstream(
    self, 
    current_item_name: str, 
    dependency_graph: dict[str, DependencyListNode], 
    tests: set[str],
    missing_items: set[str],
    current_distance: int, 
    maximum_distance: int
  ) -> None:
    # 1. If the maximum distance has been reached, the stop.
    if current_distance > maximum_distance:
      return 

    # 2. Find all the upstream items for the current item.
    current_node:DependencyListNode = dependency_graph.get(current_item_name, MissingDAGNode)

    if current_node == MissingDAGNode:
      missing_items.add(current_item_name)

    # 3. Find any upstream tests and non-test items.
    #    Missing Items will be silently skipped.
    item: Item 
    non_tests: list[Item] = []
    for item in current_node.upstream: 
      if item.name.upper().endswith('TEST'):
        tests.add(item.name)
      else: 
        non_tests.append(item)

    for upstream_item in non_tests:
      self.find_upstream(
        upstream_item.name,
        dependency_graph,  
        tests,
        missing_items,
        current_distance + 1, 
        maximum_distance)
  