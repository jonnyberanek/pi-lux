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

def get_parse_type_name(fn: ParseFunc):
  return_type = fn
  if type(return_type) is not type:
    if 'return' not in fn.__annotations__:
      raise ValueError("Parse function must be a type constructor or have an annotated return type.")
    return_type = fn.__annotations__['return']
  
  # return return_type.__module__ + "." + return_type.__name__
  return return_type.__name__
