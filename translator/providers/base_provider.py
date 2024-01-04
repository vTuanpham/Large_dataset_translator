from typing import Union, List
from abc import ABC, abstractmethod
from types import SimpleNamespace


class Provider(ABC):
    @abstractmethod
    def __init__(self):
        self.translator = None

    @abstractmethod
    def _do_translate(self, input_data: Union[str, List[str]], src: str, dest: str, **kwargs) -> Union[str, List[str]]:
        raise NotImplemented(" The function _do_translate has not been implemented.")

    def translate(self, input_data: Union[str, List[str]], src: str, dest: str) -> SimpleNamespace:
        """
        Translate text input_data from a language to another language
        :param input_data: The input_data(Can be string or list of string)
        :param src: The source lang of input_data
        :param dest: The target lang you want input_data to be translated
        :return:
        """

        assert self.translator, "Please assign the translator object instance to self.translator"
        translated_instance = self._do_translate(input_data, src=src, dest=dest)
        if not hasattr(translated_instance, 'text'):
            if isinstance(translated_instance, list) or isinstance(translated_instance, str):
                return SimpleNamespace(text=translated_instance)
            else:
                raise ValueError(f"The return object of _do_translate expected to be 'list' or 'string',"
                                 f" found {type(translated_instance)}")
        else:
            if isinstance(translated_instance.text, list) or isinstance(translated_instance.text, str):
                return translated_instance
            else:
                raise ValueError(f"The return object of _do_translate with required 'text' attribute expected to be 'list' or 'string' "
                                 f"but found {type(translated_instance.text)}")

