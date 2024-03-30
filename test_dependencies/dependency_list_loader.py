import csv
from dataclasses import dataclass
from enum import StrEnum
import os 

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
class Item:
  id: str 
  name: str
  type: str

  def __hash__(self) -> int:
    return hash((self.id, self.name, self.type))

@dataclass
class DependencyListNode:
  item: Item
  upstream: set[str]

class DependencyListLoader:
  def __init__(self) -> None:
    pass

  def load(self, filepath) -> dict[str, DependencyListNode]:
    """
    Builds an in memory direct acyclic graph as an adjacency list. 
    """
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
      raise FileNotFoundError(f'Could not find file {filepath}.')
    
    dag: dict[str, list[str]] = {}
    with open(file = filepath, newline='') as text_io:
      reader = csv.DictReader(text_io)
      for row in reader:
        item_id            = row[DependencyFileHeaders.REF_METADATA_COMPONENT_ID]
        item_name          = row[DependencyFileHeaders.REF_METADATA_COMPONENT_NAME]
        item_type          = row[DependencyFileHeaders.REF_METADATA_COMPONENT_TYPE]
        upstream_item_id   = row[DependencyFileHeaders.METADATA_COMPONENT_ID]
        upstream_item_name = row[DependencyFileHeaders.METADATA_COMPONENT_NAME]
        upstream_item_type = row[DependencyFileHeaders.METADATA_COMPONENT_TYPE]
        if item_name not in dag:
          dag[item_name] = DependencyListNode(Item(item_id, item_name, item_type), set[str]())
        dag[item_name].upstream.add(Item(upstream_item_id, upstream_item_name, upstream_item_type))
    return dag 