from dataclasses import dataclass
from typing import TypedDict, List

from pydantic import BaseModel


@dataclass
class Person:
    name: str
    backstory: str


@dataclass
class GenLore:
    names: str
    content: str


Example = str


@dataclass
class GenMessage:
    author: str
    content: str


class CharacterData(BaseModel):
    char: str
    char_info: str
    important: str
    examples: List[Example]


class GenContext(BaseModel):
    char: str
    char_info: str
    important: str
    user: str
    datetime: str
    examples: List[Example]
    persons: List[Person]
    lores: List[GenLore]
    messages: List[GenMessage]
