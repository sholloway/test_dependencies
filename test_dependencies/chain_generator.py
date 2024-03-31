from random import randint
from faker import Faker
from test_dependencies.item import Item
from test_dependencies.id_generator import IDGenerator

CLASS_SUFFIX = ['Utilities', 'Service', 'Controller', 'Handler', 'Factory', 'Generator'] 
TEST_SUFFIX = 'Test'

class ChainGenerator:
  """
  Generates a list of items that have a hierarchy. 
  This is in the form
    A <- B <- C <-... <- N
  """
  def __init__(self, id_generator: IDGenerator, text_generator: Faker, class_names_set: set[str]) -> None:
    self._id_gen = id_generator
    self._text_gen = text_generator
    self._class_names_set = class_names_set

  def generate(self, max_distance: int = 1) -> list[Item]:
    # Create Apex classes. On the last pass, create an Apex Test.
    items = []
    for current_distance in range(0, max_distance+1):
      create_test = current_distance == max_distance
      item = Item(
        id   = self._id_gen.next_id(),
        name = self._gen_class_name(test = create_test),
        type = 'ApexClass'
      )
      items.append(item)
    return items
  
  def _gen_class_name(self, test:bool = False) -> str:
    """Generates a unique class name."""
    while True: 
      words = self._text_gen.words(nb = randint(1,5))
      camel_case = [word.capitalize() for word in words]
      suffix = TEST_SUFFIX if test else CLASS_SUFFIX[randint(0,5)] 
      class_name = ''.join(camel_case) + suffix

      if class_name not in self._class_names_set:
        self._class_names_set.add(class_name)
        return class_name