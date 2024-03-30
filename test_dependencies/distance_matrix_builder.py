
from test_dependencies.item import Item
from test_dependencies.dependency_list_loader import DependencyListNode

# DistanceMatrix = dict[str, dict[int, set[Item]]]

# TODO: Rename this class.
class DistanceMatrixBuilder:
  def __init__(self) -> None:
    pass

  def build(
    self, 
    dependency_graph: dict[str, DependencyListNode], 
    changed_list: list[str], 
    maximum_distance: int
  ) -> set[Item]:
    tests = set[Item]()
    for changed_item_name in changed_list:
      self.find_upstream(
        changed_item_name, 
        dependency_graph, 
        tests,
        1, 
        maximum_distance
      )
    return tests
  
  def find_upstream(
    self, 
    current_item_name: str, 
    dependency_graph: dict[str, DependencyListNode], 
    tests: set[Item],
    current_distance: int, 
    maximum_distance: int
  ) -> None:
    # 1. If the maximum distance has been reached, the stop.
    if current_distance > maximum_distance:
      return 

    # 2. Find all the upstream items for the current item.
    current_node:DependencyListNode = dependency_graph[current_item_name]

    # 3. Find any upstream tests and non-test items.
    item: Item 
    non_tests: list[Item] = []
    for item in current_node.upstream: 
      if item.name.upper().endswith('TEST'):
        tests.add(item)
      else: 
        non_tests.append(item)

    for upstream_item in non_tests:
      self.find_upstream(
        upstream_item.name,
        dependency_graph,  
        tests,
        current_distance + 1, 
        maximum_distance)
  