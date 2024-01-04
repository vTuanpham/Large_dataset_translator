from typing import Union, List, Any
from abc import ABC, abstractmethod
from types import SimpleNamespace


class Provider(ABC):
    """
    Base Provider that must be inherited by all Provider class, implement your own provider by inheriting this class
    """
    @abstractmethod
    def __init__(self):
        self.translator = None

    @abstractmethod
    def _do_translate(self, input_data: Union[str, List[str]], src: str, dest: str, **kwargs) -> Union[str, List[str], Any]:
        raise NotImplemented(" The function _do_translate has not been implemented.")

    def translate(self, input_data: Union[str, List[str]], src: str, dest: str) -> Union[SimpleNamespace, List[SimpleNamespace]]:
        """
        Translate text input_data from a language to another language
        :param input_data: The input_data (Can be string or list of strings)
        :param src: The source lang of input_data
        :param dest: The target lang you want input_data to be translated
        :return: SimpleNamespace object or list of SimpleNamespace objects with 'text' attribute
        """

        # Type check for input_data
        if not isinstance(input_data, (str, list)):
            raise TypeError(f"input_data must be of type str or List[str], not {type(input_data).__name__}")

        if isinstance(input_data, list) and not all(isinstance(item, str) for item in input_data):
            raise TypeError("All elements of input_data list must be of type str")

        # Ensure the translator is set
        assert self.translator, "Please assign the translator object instance to self.translator"

        # Perform the translation
        translated_instance = self._do_translate(input_data, src=src, dest=dest)

        # Wrap non-list objects in SimpleNamespace if they don't have a 'text' attribute
        if not isinstance(translated_instance, list):
            if not hasattr(translated_instance, 'text'):
                return SimpleNamespace(text=translated_instance)
        else:
            # Wrap each item in the list in SimpleNamespace if the item doesn't have a 'text' attribute
            return [SimpleNamespace(text=item) if not hasattr(item, 'text') else item for item in translated_instance]

        return translated_instance

