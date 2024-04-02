from dataclasses import dataclass

@dataclass
class Item:
  id: str
  name: str
  type: str

  def __hash__(self) -> int:
    return hash((self.id, self.name, self.type))