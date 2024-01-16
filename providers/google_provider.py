import sys
from typing import Union, List
sys.path.insert(0, r'/')
from googletrans import Translator
from .base_provider import Provider


# https://github.com/ssut/py-googletrans
# This is the best reliable provider, as this has access to API call instead of using the crawling method
class GoogleProvider(Provider):
    def __init__(self):
        self.translator = Translator()

    def extract_texts(self, obj):
        '''
        Extract .text attribute from Translator object
        '''

        if isinstance(obj, list):
            return [self.extract_texts(item) for item in obj]
        else:
            try:
                return obj.text
            except AttributeError:
                return obj

    def _do_translate(self, input_data: Union[str, List[str]],
                      src: str, dest: str,
                      fail_translation_code:str = "P1OP1_F", # Pass in this code to replace the input_data if the exception is *unavoidable*, any example that contain this will be remove post translation
                      **kwargs) -> Union[str, List[str]]:
        """
        translate(text, dest='en', src='auto', **kwargs)
            Translate text from source language to destination language

            Parameters:
                text (UTF-8 str; unicode; string sequence (list, tuple, iterator, generator)) – The source text(s) to be translated. Batch translation is supported via sequence input.
                dest – The language to translate the source text into. The value should be one of the language codes listed in googletrans.LANGUAGES or one of the language names listed in googletrans.LANGCODES.
                dest – str; unicode
                src – The language of the source text. The value should be one of the language codes listed in googletrans.LANGUAGES or one of the language names listed in googletrans.LANGCODES. If a language is not specified, the system will attempt to identify the source language automatically.
                src – str; unicode
                Return type:
                Translated

            Return type: list (when a list is passed) else Translated object
        """

        data_type = "list" if isinstance(input_data, list) else "str"

        try:
            return self.extract_texts(self.translator.translate(input_data, src=src, dest=dest))
        # TypeError likely due to gender-specific translation, which has no fix yet. Please refer to
        # ssut/py-googletrans#260 for more info
        except TypeError:
            if data_type == "list": return [fail_translation_code, fail_translation_code]
            return fail_translation_code


if __name__ == '__main__':
    test = GoogleProvider()
    print(test.translate(["Hello", "How are you today ?"], src="en", dest="vi"))
    print(test.translate("Hello", src="en", dest="vi"))
