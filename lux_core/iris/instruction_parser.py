from typing import Callable, TypeAlias, TypeVar

P = TypeVar("P")

ParseFunc: TypeAlias = Callable[[str], P]

def create_list_parser(subparse: ParseFunc):
  return lambda s: [subparse(p) for p in s[1:-1].split(",")]

def parse_params(params: list[str], parse_map: list[ParseFunc]):
  """
  Usage:
  For a function with signature:
  ```
  def do_stuff(w: float, x: str, z: list[int])
  ```
  Can be called like:
  ```
  do_stuff(*parse_params(['1.0','text','[1,2]'], [float, str, create_list_parser(int)])) 
  ```
  """
  #[:len(params)] is to allow for default values to be possible when nothing provided
  return [parse(params[i].strip()) for i, parse in enumerate(parse_map[:len(params)])]