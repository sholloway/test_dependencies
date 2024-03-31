import csv
from random import randint
from faker import Faker
from test_dependencies.chain_generator import ChainGenerator
from test_dependencies.id_generator import IDGenerator

class DAGGenerator:
  CSV_HEADER=('Id','MetadataComponentId','MetadataComponentName','MetadataComponentNamespace','MetadataComponentType','RefMetadataComponentId','RefMetadataComponentName','RefMetadataComponentNamespace','RefMetadataComponentType')

  def __init__(self) -> None:
    self._id_gen = IDGenerator()
    self._text_gen = Faker()
    self._class_set: set[str] = set()
    self._chain_gen =  ChainGenerator(self._id_gen, self._text_gen, self._class_set)

  def generate(self, output_filepath: str, num_hierarchies: int, max_distance: int = 1) -> list[tuple[str,...]]:
    """
    Generates a table of metadata relationships.

    Args:
      - num_hierarchies: The number of hierarchies to generate. 
      - max_distance: The maximum distance in a hierarchy to generate.
    """
    #1. Generate a chain of classes with the specified distance. 
    hierarchies: list[list[Item]] = []
    for hierarchy in range(num_hierarchies):
      hierarchies.append(self._chain_gen.generate(max_distance=randint(1, max_distance)))

    #2. Create a dependency chain of Test -> N -> M ... -> A
    dag_rows = []
    for hierarchy in hierarchies:
      num_items = len(hierarchy)
      for position in range(num_items - 1):
        upstream_position = position + 1
        dag_row = (
          '000000000000000AAA',
          hierarchy[upstream_position].id, 
          hierarchy[upstream_position].name, 
          '',
          hierarchy[upstream_position].type, 
          hierarchy[position].id, 
          hierarchy[position].name, 
          '',
          hierarchy[position].type
        )
        dag_rows.append(dag_row)

    # 3. Write the rows
    
    with open(output_filepath, 'w', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(DAGGenerator.CSV_HEADER)
      writer.writerows(dag_rows)

    return dag_rows