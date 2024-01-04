import sys
from typing import Union, List
sys.path.insert(0, r'./')
from googletrans import Translator
from .base_provider import Provider


class GoogleProvider(Provider):
    def __init__(self):
        self.translator = Translator()

    def _do_translate(self, input_data: Union[str, List[str]], src: str, dest: str, **kwargs) -> Union[str, List[str]]:
        return self.translator.translate(input_data, src=src, dest=dest)


if __name__ == '__main__':
    test = GoogleProvider()
    print(test.translate("Hello", src="en", dest="vi").text)
