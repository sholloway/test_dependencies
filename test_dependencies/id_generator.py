from test_dependencies.base62 import Base62

class IDGenerationError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

class IDGenerator:
  """Create an increasing series of fake Salesforce IDs."""
  def __init__(self, starting_id: int = 0) -> None:
    self._last_id = starting_id
    self._base62 = Base62()

  def next_id(self, prefix: str = '01p', host: str = '0M', checksum: str = 'QAY') -> str:
    """
    Generates a sequential fake ID in the style of 18 character Salesforce IDs.

    Returns an 18 character string of the format:
    PREFIX + INSTANCE + 0 + PADDED BASE62 POSITIVE NUMBER + CHECKSUM 

    Note: The CHECKSUM is a static value. It is not used by this application.

    Args:
      prefix: A 3 character string that maps to a Salesforce metadata prefix.
      host: A two character string that maps to a Salesforce pod. 
      checksum: A three character string that is appended to the ID. Real IDs calculate a checksum.
    """
    if len(prefix) != 3:
      raise IDGenerationError(f'The ID prefix must be exactly 3 characters. A prefix of length {len(prefix)} was provided.')
    
    if len(host) != 2:
      raise IDGenerationError(f'The ID host must be exactly 2 characters. A host of length {len(host)} was provided.')
    
    if len(checksum) != 3:
      raise IDGenerationError(f'The ID checksum must be exactly 3 characters. A checksum of length {len(checksum)} was provided.')
    
    self._last_id += 1
    encoded_id = self._base62.encode(self._last_id)
    padded_encoded_id = encoded_id.rjust(9,'0')
    return prefix + host + '0' + padded_encoded_id + checksum