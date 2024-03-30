import argparse

class OptionsProcessor:
  """Processes the application command line options."""
  def __init__(self) -> None:
    self._parser = argparse.ArgumentParser(description='Find Salesforce Test Dependencies')
    self._options: dict | None = None
    self._register_options()

  def options(self) -> dict:
    if self._options is None:
      raise RuntimeError('Options not parsed. Call OptionsProcessor.process() before options()')
    return self._options
  
  def process(self) -> dict:
    self._options = vars(self._parser.parse_args())
    return self._options

  def _register_options(self):
    """Register the command line options."""
    # Required option to set the dependency list.
    self._parser.add_argument(
      '-dl',
      '--dependency_list', 
      required = True,
      type     = str, 
      dest     = 'dependency_list', 
      help     = 'The CSV file of dependencies to use.'
    )

    # Required option to set the list of changed files.
    self._parser.add_argument(
      '-cl',
      '--changed_list', 
      required = True,
      type     = str, 
      dest     = 'changed_list', 
      help     = 'The text file that lists the Apex classes that changed.'
    )

    # Option to set the number of relationship degrees to explore when 
    # identifying which tests to run.
    self._parser.add_argument(
      '-d',
      '--degrees', 
      required = False,
      type     = int, 
      default  = 1,
      dest     = 'degrees', 
      help     = 'The number of relationship degrees to explore when identifying which tests to run.'
    )