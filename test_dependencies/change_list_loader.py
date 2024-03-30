
import os


class ChangeListLoader:
  def __init__(self) -> None:
    pass

  def load(self, filepath:str) -> list[str]:
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
      raise FileNotFoundError(f'Could not find file {filepath}.')
    with open(file = filepath) as text_io:
      change_list = [line.rstrip() for line in text_io]
    return change_list
