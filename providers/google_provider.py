import sys
import asyncio
from typing import Union, List
sys.path.insert(0, r'/')
from googletrans import Translator
from googletrans.models import Translated
import platform

if platform.system() == "Windows":
    print("Setting WindowsSelectorEventLoopPolicy for asyncio on Windows")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

try:
    from .base_provider import Provider
except ImportError:
    from base_provider import Provider

# https://github.com/ssut/py-googletrans
# This is the best reliable provider, as this has access to API call instead of using the crawling method
class GoogleProvider(Provider):
    def __init__(self):
        self.translator = Translator()
        # Store a shared event loop for reuse
        try:
            self._loop = asyncio.get_event_loop()
            if self._loop.is_closed():
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

    def extract_texts(self, obj: Union[Translated, List[Translated], None]) -> Union[str, List[str]]:
        """
        Extract .text attribute from Translated object
        """
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
        
        # Skip translation if source and destination languages are the same
        if src == dest:
            print(f"Warning: Source language ({src}) and destination language ({dest}) are the same. Skipping translation.")
            return input_data

        try:
            # Run the translation in the shared event loop
            if data_type == "list":
                async def translate_list():
                    results = []
                    for text in input_data:
                        try:
                            result = await self.translator.translate(text, src=src, dest=dest)
                            results.append(result)
                        except Exception as e:
                            print(f"Error translating list item: {e}")
                            results.append(None)
                    return results
                
                if self._loop.is_running():
                    future = asyncio.run_coroutine_threadsafe(translate_list(), self._loop)
                    translated = future.result(30)  # 30 second timeout
                else:
                    translated = self._loop.run_until_complete(translate_list())
                
                # Filter out None values and extract text
                valid_results = [item for item in translated if item is not None]
                if not valid_results:
                    return [fail_translation_code] * len(input_data)
                    
                return self.extract_texts(valid_results)
            else:
                async def translate_single():
                    return await self.translator.translate(input_data, src=src, dest=dest)
                
                if self._loop.is_running():
                    future = asyncio.run_coroutine_threadsafe(translate_single(), self._loop)
                    translated = future.result(30)  # 30 second timeout
                else:
                    translated = self._loop.run_until_complete(translate_single())
                
                return self.extract_texts(translated)
        # TypeError likely due to gender-specific translation, which has no fix yet. Please refer to
        # ssut/py-googletrans#260 for more info
        except TypeError as e:
            # print(f"Translation TypeError: {e}")
            if data_type == "list": 
                return [fail_translation_code] * len(input_data)
            return fail_translation_code
            
        except Exception as e:
            # print(f"Translation error: {e}")
            if data_type == "list": 
                return [fail_translation_code] * len(input_data)
            return fail_translation_code


if __name__ == '__main__':
    test = GoogleProvider()
    print(test.translate(["Hello", "How are you today ?"], src="en", dest="vi"))
    print(test.translate("Hello", src="en", dest="vi"))