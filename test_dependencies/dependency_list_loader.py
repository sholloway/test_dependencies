import csv
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

class DependencyListLoader:
  def __init__(self) -> None:
    pass

  def load(self, filepath) -> dict[str, list[str]]:
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
      raise FileNotFoundError(f'Could not find file {filepath}.')
    
    with open(file = filepath, newline='') as text_io:
      reader = csv.DictReader(text_io)
      for row in reader:
        print(row['id'])
