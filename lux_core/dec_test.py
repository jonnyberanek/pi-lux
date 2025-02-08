from abc import ABC, abstractmethod
import collections
import collections.abc
import json
import types
from typing import Callable, Generic, TypeAlias, TypeVar, ParamSpec
import inspect
import typing

from collections import namedtuple

import json.scanner

P = ParamSpec("P")
R = TypeVar("R")

def get_annotations(func):
  sig = inspect.signature(func)
  annos = [sig.parameters[k].annotation for k in sig.parameters]
  for i, a in enumerate(annos):
      gen = typing.get_args(a)
      print(type(a))
      if len(gen):
          annos[i] = (list, a)
      # if a == list:
          print("is list")
  return annos
      # p = sig.parameters[k]
      # print(p.name, p.kind, p.annotation, p.annotation)
      # # if(p.annotation == str):
      # print(f"{p.annotation(1)!r}")

def add_logging(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
            
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

# @add_logging
def my_function(a: int, b: list[int]) -> float:
    return a + b[0]

# json.scanner.make_scanner

# annos = get_annotations(my_function)
# print(annos)

# args = ["1", ["2.5"]]
# # parsed_args = args
# parsed_args = [annos[i](a) for i, a in enumerate(args)]

# print(parsed_args)

# result = my_function(*parsed_args)

# print(result)

# p = list[str]
# print(p)
# print(type(p))
# # print(dir(p))

# print(typing.get_args(p))

# class plist():
#     def __init__(self, t):
#         self.type = t


P = TypeVar("P")
T = TypeVar("T")

class ParamParser(Generic[P]):
  def parse(self, s: str) -> P:
    pass

ParamParser()

def create_param_parser(fn):
  parser = ParamParser()
  parser.parse = fn
  return parser

class ListParamParser(ParamParser[list[T]]):
  def __init__(self, nested_parser: ParamParser[T]):
     self.nested_parser = nested_parser
     super().__init__()

  def parse(self, s) -> list[T]:
     return [self.nested_parser.parse(p) for p in s[1:-1].split(",")]

# class PrimitiveParser():
#   INT = create_param_parser(int)
#   FLOAT = create_param_parser(float)
#   STRING = create_param_parser(str)

ParseFunc: TypeAlias = Callable[[str], P]

def create_list_parser(subparse: ParseFunc):
  return lambda s: [subparse(p) for p in s[1:-1].split(",")]

class PrimitiveParser():
  INT = int
  FLOAT = float
  STRING = str

def parse(params: list[str], map: list[ParseFunc]):
  return [map[i](p.strip()) for i, p in enumerate(params)]

arg_types = [float, str, int, create_list_parser(int)]
def do_stuff(w: float, x: str, y: int, z: list[int]):
    print(x + " is " + str(w + y + sum(z)))

# arg_types = [PrimParser.FLOAT, PrimParser.STRING, PrimParser.INT]
# def do_stuff(w: float, x: str, y: int):
#     print(x + " is " + str(w + y))

annos = get_annotations(do_stuff)

do_stuff(1.1, "asdfasdf", 1, [4,5])

params = " 1.1   ;  as  dfdf   ;1 ;   [  4    ,5  ]"

params = params.split(";")

do_stuff(*parse(params, arg_types))
# params.