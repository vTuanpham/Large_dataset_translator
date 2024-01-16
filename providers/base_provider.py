from typing import Union, List
from abc import ABC, abstractmethod


class Provider(ABC):
    """
    Base Provider that must be inherited by all Provider class, implement your own provider by inheriting this class
    """
    @abstractmethod
    def __init__(self):
        self.translator = None

    @abstractmethod
    def _do_translate(self, input_data: Union[str, List[str]],
                      src: str, dest: str,
                      fail_translation_code:str = "P1OP1_F",
                      **kwargs) -> Union[str, List[str]]:
        raise NotImplemented(" The function _do_translate has not been implemented.")

    def translate(self, input_data: Union[str, List[str]],
                  src: str, dest: str,
                  fail_translation_code: str="P1OP1_F") -> Union[str, List[str]]:
        """
        Translate text input_data from a language to another language
        :param input_data: The input_data (Can be string or list of strings)
        :param src: The source lang of input_data
        :param dest: The target lang you want input_data to be translated
        :param fail_translation_code: The code that can be use for unavoidable translation error and can be remove post translation
        :return: str or list of str
        """

        # Type check for input_data
        if not isinstance(input_data, (str, list)):
            raise TypeError(f"input_data must be of type str or List[str], not {type(input_data).__name__}")

        if isinstance(input_data, list) and not all(isinstance(item, str) for item in input_data):
            raise TypeError("All elements of input_data list must be of type str")

        # Ensure the translator is set
        assert self.translator, "Please assign the translator object instance to self.translator"

        # Perform the translation
        translated_instance = self._do_translate(input_data,
                                                 src=src, dest=dest,
                                                 fail_translation_code=fail_translation_code)

        assert type(input_data) == type(translated_instance),\
            f" The function self._do_translate() return mismatch datatype from the input_data," \
            f" expected {type(input_data)} from self._do_translate() but got {type(translated_instance)}"

        return translated_instance


