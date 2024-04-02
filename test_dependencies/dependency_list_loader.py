import csv
from dataclasses import dataclass
from enum import StrEnum
import os

from test_dependencies.item import Item 

class DependencyFileHeaders(StrEnum):
  ID = 'Id'
  METADATA_COMPONENT_ID            = 'MetadataComponentId'
  METADATA_COMPONENT_NAME          = 'MetadataComponentName'
  METADATA_COMPONENT_NAMESPACE     = 'MetadataComponentNamespace'
  METADATA_COMPONENT_TYPE          = 'MetadataComponentType'
  REF_METADATA_COMPONENT_ID        = 'RefMetadataComponentId'
  REF_METADATA_COMPONENT_NAME      = 'RefMetadataComponentName'
  REF_METADATA_COMPONENT_NAMESPACE = 'RefMetadataComponentNamespace'
  REF_METADATA_COMPONENT_TYPE      = 'RefMetadataComponentType'

@dataclass
class DependencyListNode:
  item: Item
  upstream: set[Item]

AdjacencyListType = dict[str, DependencyListNode]
class DependencyListLoader:
  def __init__(self) -> None:
    self._test_counter = 0
    self._apex_class_counter = 0

  @property
  def num_tests(self) -> int:
    return self._test_counter
  
  @property
  def num_apex_classes(self) -> int:
    return self._apex_class_counter

  def load(self, filepath) -> AdjacencyListType:
    """
    Builds an in memory direct acyclic graph as an adjacency list. 
    """
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
      raise FileNotFoundError(f'Could not find file {filepath}.')
    
    dag: AdjacencyListType = {}
    unique_test_name        = set[str]()
    unique_apex_class_name  = set[str]()

    with open(file = filepath, newline='') as text_io:
      reader = csv.DictReader(text_io)
      for row in reader:
        item_id            = row[DependencyFileHeaders.REF_METADATA_COMPONENT_ID]
        item_name          = row[DependencyFileHeaders.REF_METADATA_COMPONENT_NAME]
        item_type          = row[DependencyFileHeaders.REF_METADATA_COMPONENT_TYPE]
        upstream_item_id   = row[DependencyFileHeaders.METADATA_COMPONENT_ID]
        upstream_item_name = row[DependencyFileHeaders.METADATA_COMPONENT_NAME]
        upstream_item_type = row[DependencyFileHeaders.METADATA_COMPONENT_TYPE]

        if item_name not in unique_test_name:
          unique_apex_class_name.add(item_name)
        
        if upstream_item_name.upper().endswith('TEST') and upstream_item_name not in unique_test_name:
          unique_test_name.add(upstream_item_name)

        if item_name not in dag:
          dag[item_name] = DependencyListNode(Item(item_id, item_name, item_type), set[Item]())
        dag[item_name].upstream.add(Item(upstream_item_id, upstream_item_name, upstream_item_type))

    self._test_counter = len(unique_test_name)
    self._apex_class_counter = len(unique_apex_class_name)
    return dag 