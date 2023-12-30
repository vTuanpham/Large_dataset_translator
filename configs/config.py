import sys
sys.path.insert(0,r'./')
import pprint
from abc import ABC, abstractmethod
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Config(ABC):
    """
    Abstract config that must be inherited by all configs class
    """

    qas_id: str  # Required field in all subclass

    def __str__(self) -> str:
        return self.__repr__

    @property
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @property
    @abstractmethod
    def get_dict(self) -> Dict:
        pass

    @classmethod
    @abstractmethod
    def get_keys(cls) -> List[str]:
        pass

    @property
    def get_dict_str(self, indent: int=4) -> None:
        pp = pprint.PrettyPrinter(indent=indent)
        pp.pprint(self.get_dict)

