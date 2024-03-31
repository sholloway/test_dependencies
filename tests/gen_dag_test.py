
from random import randint
from faker import Faker 

"""
Item Name: These need to be unique and consistent.
Item ID: Salesforce ID
Item Type: Parameter

Tests end with the suffix Test

Classes can be Utilities, Service, Controller, Handler, Trigger, Test.
"""
from test_dependencies.item import Item
from test_dependencies.id_generator import IDGenerator

class DAGGenerator:
  CLASS_SUFFIX = ['Utilities', 'Service', 'Controller', 'Handler', 'Factory', 'Generator'] 
  TEST_SUFFIX = 'Test'

  def __init__(self) -> None:
    self._id_gen = IDGenerator()
    self._text_gen = Faker()
    self._class_set: set[str] = set()

  def generate(self, max_distance: int = 1) -> list[tuple[str,...]]:
    #1. Create Apex classes. On the last pass, create an Apex Test.
    items = []
    for current_distance in range(0, max_distance+1):
      create_test = current_distance == max_distance
      item = Item(
        id   = self._id_gen.next_id(),
        name = self.gen_class_name(test = create_test),
        type = 'ApexClass'
      )
      items.append(item)

    #2. Create a dependency chain of Test -> N -> M ... -> A
    dag_rows = []
    num_items = len(items)
    for position in range(num_items):
      upstream_position = (position + 1) % num_items 
      dag_row = (
        '000000000000000AAA',
        items[upstream_position].id, 
        items[upstream_position].name, 
        '',
        items[upstream_position].type, 
        items[position].id, 
        items[position].name, 
        '',
        items[position].type
      )
      dag_rows.append(dag_row)
    return dag_row
  
  def gen_class_name(self, test:bool = False) -> str:
    """Generates a unique class name."""
    while True: 
      words = self._text_gen.words(nb = randint(1,5))
      camel_case = [word.capitalize() for word in words]
      suffix = DAGGenerator.TEST_SUFFIX if test else DAGGenerator.CLASS_SUFFIX[randint(0,5)] 
      class_name = ''.join(camel_case) + suffix

      if class_name not in self._class_set:
        self._class_set.add(class_name)
        return class_name

class TestGenDagFile:
  def test_gen_class_names(self) -> None:
    gen = DAGGenerator()
    rows = gen.generate(max_distance=1)
    print(rows)
    assert False
  
  
    